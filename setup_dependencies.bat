@echo off
echo ========================================
echo Настройка системы управления зависимостями
echo ========================================

echo Создание виртуального окружения...
python -m venv venv

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Обновление pip...
python -m pip install --upgrade pip

echo Установка основных зависимостей...
pip install aiogram==3.3.0
pip install openai==1.12.0
pip install chromadb==0.4.22
pip install PyMuPDF==1.23.14
pip install python-dotenv==1.0.0
pip install httpx==0.26.0
pip install numpy==1.26.4
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2
pip install aiohttp==3.9.1
pip install lxml==4.9.3
pip install python-docx==0.8.11
pip install Flask==3.0.0
pip install Flask-Cors==4.0.0
pip install psutil==5.9.6
pip install scikit-learn==1.7.0
pip install pandas==2.3.1
pip install scipy==1.15.3

echo Создание requirements.txt...
pip freeze > requirements.txt

echo Создание requirements.minimal.txt...
echo aiogram==3.3.0 > requirements.minimal.txt
echo openai==1.12.0 >> requirements.minimal.txt
echo chromadb==0.4.22 >> requirements.minimal.txt
echo PyMuPDF==1.23.14 >> requirements.minimal.txt
echo python-dotenv==1.0.0 >> requirements.minimal.txt
echo httpx==0.26.0 >> requirements.minimal.txt
echo numpy==1.26.4 >> requirements.minimal.txt
echo requests==2.31.0 >> requirements.minimal.txt
echo beautifulsoup4==4.12.2 >> requirements.minimal.txt
echo aiohttp==3.9.1 >> requirements.minimal.txt
echo lxml==4.9.3 >> requirements.minimal.txt
echo python-docx==0.8.11 >> requirements.minimal.txt
echo Flask==3.0.0 >> requirements.minimal.txt
echo Flask-Cors==4.0.0 >> requirements.minimal.txt
echo psutil==5.9.6 >> requirements.minimal.txt
echo scikit-learn==1.7.0 >> requirements.minimal.txt
echo pandas==2.3.1 >> requirements.minimal.txt
echo scipy==1.15.3 >> requirements.minimal.txt

echo Установка pre-commit...
pip install pre-commit

echo Настройка pre-commit...
pre-commit install

echo ========================================
echo Настройка завершена!
echo ========================================
echo.
echo Что было сделано:
echo - Создано виртуальное окружение venv
echo - Установлены основные зависимости
echo - Создан requirements.txt
echo - Создан requirements.minimal.txt
echo - Установлен и настроен pre-commit
echo.
echo Теперь вы можете:
echo - Запускать update_requirements.bat для обновления зависимостей
echo - Использовать pre-commit для автоматической проверки
echo - Работать с виртуальным окружением
echo.
pause 