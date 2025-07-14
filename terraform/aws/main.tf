terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "legal-bot-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
resource "aws_vpc" "legal_bot_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "legal-bot-vpc"
    Environment = "production"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "legal_bot_igw" {
  vpc_id = aws_vpc.legal_bot_vpc.id

  tags = {
    Name        = "legal-bot-igw"
    Environment = "production"
  }
}

# Public Subnets
resource "aws_subnet" "public_subnets" {
  count                   = 2
  vpc_id                  = aws_vpc.legal_bot_vpc.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name        = "legal-bot-public-subnet-${count.index + 1}"
    Environment = "production"
  }
}

# Private Subnets
resource "aws_subnet" "private_subnets" {
  count             = 2
  vpc_id            = aws_vpc.legal_bot_vpc.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name        = "legal-bot-private-subnet-${count.index + 1}"
    Environment = "production"
  }
}

# Route Table for Public Subnets
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.legal_bot_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.legal_bot_igw.id
  }

  tags = {
    Name        = "legal-bot-public-rt"
    Environment = "production"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public_rta" {
  count          = length(aws_subnet.public_subnets)
  subnet_id      = aws_subnet.public_subnets[count.index].id
  route_table_id = aws_route_table.public_rt.id
}

# Security Groups
resource "aws_security_group" "alb_sg" {
  name        = "legal-bot-alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = aws_vpc.legal_bot_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "legal-bot-alb-sg"
    Environment = "production"
  }
}

resource "aws_security_group" "ecs_sg" {
  name        = "legal-bot-ecs-sg"
  description = "Security group for ECS tasks"
  vpc_id      = aws_vpc.legal_bot_vpc.id

  ingress {
    from_port       = 5000
    to_port         = 5000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "legal-bot-ecs-sg"
    Environment = "production"
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "legal-bot-rds-sg"
  description = "Security group for RDS database"
  vpc_id      = aws_vpc.legal_bot_vpc.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_sg.id]
  }

  tags = {
    Name        = "legal-bot-rds-sg"
    Environment = "production"
  }
}

# Application Load Balancer
resource "aws_lb" "legal_bot_alb" {
  name               = "legal-bot-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = aws_subnet.public_subnets[*].id

  enable_deletion_protection = false

  tags = {
    Name        = "legal-bot-alb"
    Environment = "production"
  }
}

# Target Group
resource "aws_lb_target_group" "legal_bot_tg" {
  name        = "legal-bot-tg"
  port        = 5000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.legal_bot_vpc.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }

  tags = {
    Name        = "legal-bot-tg"
    Environment = "production"
  }
}

# ALB Listener
resource "aws_lb_listener" "legal_bot_listener" {
  load_balancer_arn = aws_lb.legal_bot_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.legal_bot_tg.arn
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "legal_bot_cluster" {
  name = "legal-bot-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name        = "legal-bot-cluster"
    Environment = "production"
  }
}

# ECS Task Definition
resource "aws_ecs_task_definition" "legal_bot_task" {
  family                   = "legal-bot"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "legal-bot"
      image = "${aws_ecr_repository.legal_bot_repo.repository_url}:latest"
      
      portMappings = [
        {
          containerPort = 5000
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "ENVIRONMENT"
          value = "production"
        },
        {
          name  = "REDIS_URL"
          value = "redis://${aws_elasticache_cluster.legal_bot_redis.cache_nodes[0].address}:6379"
        }
      ]
      
      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_secretsmanager_secret.database_url.arn
        },
        {
          name      = "JWT_SECRET"
          valueFrom = aws_secretsmanager_secret.jwt_secret.arn
        },
        {
          name      = "OPENAI_API_KEY"
          valueFrom = aws_secretsmanager_secret.openai_api_key.arn
        }
      ]
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.legal_bot_logs.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      
      essential = true
    }
  ])

  tags = {
    Name        = "legal-bot-task"
    Environment = "production"
  }
}

# ECS Service
resource "aws_ecs_service" "legal_bot_service" {
  name            = "legal-bot-service"
  cluster         = aws_ecs_cluster.legal_bot_cluster.id
  task_definition = aws_ecs_task_definition.legal_bot_task.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private_subnets[*].id
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.legal_bot_tg.arn
    container_name   = "legal-bot"
    container_port   = 5000
  }

  depends_on = [aws_lb_listener.legal_bot_listener]

  tags = {
    Name        = "legal-bot-service"
    Environment = "production"
  }
}

# RDS Subnet Group
resource "aws_db_subnet_group" "legal_bot_db_subnet_group" {
  name       = "legal-bot-db-subnet-group"
  subnet_ids = aws_subnet.private_subnets[*].id

  tags = {
    Name        = "legal-bot-db-subnet-group"
    Environment = "production"
  }
}

# RDS Instance
resource "aws_db_instance" "legal_bot_db" {
  identifier     = "legal-bot-db"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp2"
  storage_encrypted     = true
  
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.legal_bot_db_subnet_group.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "legal-bot-db-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  
  deletion_protection = true
  
  tags = {
    Name        = "legal-bot-db"
    Environment = "production"
  }
}

# ElastiCache Subnet Group
resource "aws_elasticache_subnet_group" "legal_bot_redis_subnet_group" {
  name       = "legal-bot-redis-subnet-group"
  subnet_ids = aws_subnet.private_subnets[*].id

  tags = {
    Name        = "legal-bot-redis-subnet-group"
    Environment = "production"
  }
}

# ElastiCache Redis Cluster
resource "aws_elasticache_cluster" "legal_bot_redis" {
  cluster_id           = "legal-bot-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.legal_bot_redis_subnet_group.name
  security_group_ids   = [aws_security_group.rds_sg.id]

  tags = {
    Name        = "legal-bot-redis"
    Environment = "production"
  }
}

# ECR Repository
resource "aws_ecr_repository" "legal_bot_repo" {
  name                 = "legal-bot"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "legal-bot-repo"
    Environment = "production"
  }
}

# S3 Bucket for file storage
resource "aws_s3_bucket" "legal_bot_storage" {
  bucket = "legal-bot-storage-${random_id.bucket_suffix.hex}"

  tags = {
    Name        = "legal-bot-storage"
    Environment = "production"
  }
}

resource "aws_s3_bucket_versioning" "legal_bot_storage_versioning" {
  bucket = aws_s3_bucket.legal_bot_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_encryption" "legal_bot_storage_encryption" {
  bucket = aws_s3_bucket.legal_bot_storage.id

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "legal_bot_logs" {
  name              = "/ecs/legal-bot"
  retention_in_days = 30

  tags = {
    Name        = "legal-bot-logs"
    Environment = "production"
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

resource "random_id" "bucket_suffix" {
  byte_length = 8
} 