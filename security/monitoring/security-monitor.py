#!/usr/bin/env python3
"""
Security monitoring script for Legal Bot
Monitors logs, detects anomalies, and sends alerts
"""

import os
import re
import json
import time
import smtplib
import logging
from datetime import datetime, timedelta
from collections import defaultdict, deque
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import requests
import psutil

# Configuration
CONFIG = {
    'log_files': [
        '/var/log/nginx/access.log',
        '/var/log/nginx/error.log',
        '/app/logs/auth.log',
        '/app/logs/api.log',
        '/app/logs/app.log'
    ],
    'alert_thresholds': {
        'failed_auth_per_minute': 10,
        'error_rate_per_minute': 50,
        'cpu_usage_percent': 80,
        'memory_usage_percent': 85,
        'disk_usage_percent': 90,
        'suspicious_requests_per_minute': 20
    },
    'email': {
        'smtp_server': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'username': os.getenv('SMTP_USER'),
        'password': os.getenv('SMTP_PASSWORD'),
        'from_email': os.getenv('SMTP_FROM_ADDRESS'),
        'to_emails': os.getenv('SECURITY_ALERT_EMAILS', '').split(',')
    },
    'slack_webhook': os.getenv('SLACK_SECURITY_WEBHOOK'),
    'check_interval': 60  # seconds
}

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/security-monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecurityMonitor:
    def __init__(self):
        self.ip_requests = defaultdict(lambda: deque(maxlen=100))
        self.failed_auth_attempts = defaultdict(lambda: deque(maxlen=50))
        self.error_counts = deque(maxlen=100)
        self.suspicious_patterns = [
            r'(?i)(union.*select|insert.*into|delete.*from|drop.*table)',
            r'(?i)(<script|javascript:|vbscript:|onload|onerror|onclick)',
            r'(?i)(\.\.\/|\.\.\\|\/etc\/passwd|\/etc\/shadow)',
            r'(?i)(wp-admin|wp-login|phpmyadmin|admin\.php)',
            r'(?i)(sqlmap|nmap|masscan|nikto|dirb|dirbuster)',
            r'(?i)(python-requests|python-urllib|libwww-perl)',
            r'(?i)(bot|crawler|spider|scraper)(?!.*google|.*bing)',
        ]
        self.last_positions = {}
        
    def read_log_file(self, filepath):
        """Read new lines from log file"""
        try:
            if not os.path.exists(filepath):
                return []
                
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                # Get current position
                current_pos = f.tell()
                f.seek(0, 2)  # Go to end
                file_size = f.tell()
                
                # Check if file was rotated
                if filepath in self.last_positions:
                    if file_size < self.last_positions[filepath]:
                        # File was rotated, start from beginning
                        self.last_positions[filepath] = 0
                    f.seek(self.last_positions[filepath])
                else:
                    # First time reading, start from end
                    self.last_positions[filepath] = file_size
                    return []
                
                # Read new lines
                new_lines = f.readlines()
                self.last_positions[filepath] = f.tell()
                
                return new_lines
                
        except Exception as e:
            logger.error(f"Error reading log file {filepath}: {e}")
            return []
    
    def analyze_nginx_access_log(self, lines):
        """Analyze nginx access log for suspicious activity"""
        suspicious_ips = set()
        current_time = datetime.now()
        
        for line in lines:
            # Parse nginx log format
            match = re.match(
                r'(\S+) - \S+ \[(.*?)\] "(\S+) (\S+) \S+" (\d+) \d+ ".*?" ".*?"',
                line
            )
            
            if match:
                ip, timestamp, method, url, status = match.groups()
                
                # Track requests per IP
                self.ip_requests[ip].append(current_time)
                
                # Check for suspicious patterns
                for pattern in self.suspicious_patterns:
                    if re.search(pattern, url):
                        suspicious_ips.add(ip)
                        logger.warning(f"Suspicious request from {ip}: {url}")
                
                # Check for error status codes
                if status in ['400', '401', '403', '404', '429', '500', '502', '503', '504']:
                    self.error_counts.append(current_time)
        
        return suspicious_ips
    
    def analyze_auth_log(self, lines):
        """Analyze authentication log for failed attempts"""
        failed_ips = set()
        current_time = datetime.now()
        
        for line in lines:
            if 'authentication failed' in line.lower() or 'invalid credentials' in line.lower():
                # Extract IP from log line
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    ip = ip_match.group(1)
                    self.failed_auth_attempts[ip].append(current_time)
                    failed_ips.add(ip)
        
        return failed_ips
    
    def check_system_resources(self):
        """Check system resource usage"""
        alerts = []
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > CONFIG['alert_thresholds']['cpu_usage_percent']:
            alerts.append(f"High CPU usage: {cpu_percent}%")
        
        # Memory usage
        memory = psutil.virtual_memory()
        if memory.percent > CONFIG['alert_thresholds']['memory_usage_percent']:
            alerts.append(f"High memory usage: {memory.percent}%")
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent > CONFIG['alert_thresholds']['disk_usage_percent']:
            alerts.append(f"High disk usage: {disk_percent:.1f}%")
        
        return alerts
    
    def check_rate_limits(self):
        """Check for rate limit violations"""
        alerts = []
        current_time = datetime.now()
        minute_ago = current_time - timedelta(minutes=1)
        
        # Check failed auth attempts
        for ip, attempts in self.failed_auth_attempts.items():
            recent_attempts = [t for t in attempts if t > minute_ago]
            if len(recent_attempts) > CONFIG['alert_thresholds']['failed_auth_per_minute']:
                alerts.append(f"High failed auth attempts from {ip}: {len(recent_attempts)}/min")
        
        # Check error rate
        recent_errors = [t for t in self.error_counts if t > minute_ago]
        if len(recent_errors) > CONFIG['alert_thresholds']['error_rate_per_minute']:
            alerts.append(f"High error rate: {len(recent_errors)}/min")
        
        # Check suspicious requests
        for ip, requests in self.ip_requests.items():
            recent_requests = [t for t in requests if t > minute_ago]
            if len(recent_requests) > CONFIG['alert_thresholds']['suspicious_requests_per_minute']:
                alerts.append(f"High request rate from {ip}: {len(recent_requests)}/min")
        
        return alerts
    
    def send_email_alert(self, subject, message):
        """Send email alert"""
        try:
            if not CONFIG['email']['username'] or not CONFIG['email']['to_emails']:
                return
            
            msg = MIMEMultipart()
            msg['From'] = CONFIG['email']['from_email']
            msg['To'] = ', '.join(CONFIG['email']['to_emails'])
            msg['Subject'] = f"[Legal Bot Security Alert] {subject}"
            
            body = f"""
Security Alert for Legal Bot

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Alert: {subject}

Details:
{message}

Please investigate immediately.

--
Legal Bot Security Monitor
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(CONFIG['email']['smtp_server'], CONFIG['email']['smtp_port'])
            server.starttls()
            server.login(CONFIG['email']['username'], CONFIG['email']['password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email alert sent: {subject}")
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
    
    def send_slack_alert(self, message):
        """Send Slack alert"""
        try:
            if not CONFIG['slack_webhook']:
                return
            
            payload = {
                'text': f"🚨 Legal Bot Security Alert",
                'attachments': [
                    {
                        'color': 'danger',
                        'fields': [
                            {
                                'title': 'Alert Details',
                                'value': message,
                                'short': False
                            },
                            {
                                'title': 'Time',
                                'value': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'short': True
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(CONFIG['slack_webhook'], json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info("Slack alert sent")
            
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
    
    def run_security_check(self):
        """Run a complete security check"""
        logger.info("Running security check...")
        
        all_alerts = []
        
        # Check log files
        for log_file in CONFIG['log_files']:
            lines = self.read_log_file(log_file)
            
            if 'access.log' in log_file:
                suspicious_ips = self.analyze_nginx_access_log(lines)
                if suspicious_ips:
                    all_alerts.append(f"Suspicious activity from IPs: {', '.join(suspicious_ips)}")
            
            elif 'auth.log' in log_file:
                failed_ips = self.analyze_auth_log(lines)
                if failed_ips:
                    all_alerts.append(f"Failed auth attempts from IPs: {', '.join(failed_ips)}")
        
        # Check system resources
        resource_alerts = self.check_system_resources()
        all_alerts.extend(resource_alerts)
        
        # Check rate limits
        rate_alerts = self.check_rate_limits()
        all_alerts.extend(rate_alerts)
        
        # Send alerts if any
        if all_alerts:
            alert_message = '\n'.join(all_alerts)
            logger.warning(f"Security alerts: {alert_message}")
            
            self.send_email_alert("Security Threats Detected", alert_message)
            self.send_slack_alert(alert_message)
        
        logger.info("Security check completed")
    
    def run(self):
        """Main monitoring loop"""
        logger.info("Starting security monitor...")
        
        while True:
            try:
                self.run_security_check()
                time.sleep(CONFIG['check_interval'])
                
            except KeyboardInterrupt:
                logger.info("Security monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in security monitor: {e}")
                time.sleep(CONFIG['check_interval'])

if __name__ == "__main__":
    monitor = SecurityMonitor()
    monitor.run() 