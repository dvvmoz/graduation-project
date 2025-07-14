#!/bin/bash
# Проверка и активация venv
if [ -z "$VIRTUAL_ENV" ]; then
  echo "Активация виртуального окружения..."
  source ./venv/bin/activate
  # Перезапуск скрипта уже внутри venv
  exec "$0" "$@"
  exit
fi 