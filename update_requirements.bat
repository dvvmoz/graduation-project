@echo off
echo ========================================
echo Обновление requirements.txt из venv
echo ========================================

REM Проверяем существование виртуального окружения
if not exist "venv\Scripts\activate.bat" (
    echo ОШИБКА: Виртуальное окружение не найдено!
    echo Создайте виртуальное окружение: python -m venv venv
    pause
    exit /b 1
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Обновление pip...
python -m pip install --upgrade pip

echo Создание полного requirements.txt...
pip freeze > requirements.txt

echo Создание минимального requirements.minimal.txt...
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

echo Создание backup файла...
copy requirements.txt requirements.backup.txt

echo ========================================
echo Обновление завершено!
echo ========================================
echo.
echo Файлы обновлены:
echo - requirements.txt (полный список)
echo - requirements.minimal.txt (минимальный набор)
echo - requirements.backup.txt (резервная копия)
echo.
echo Количество пакетов в requirements.txt:
find /c "==" requirements.txt
echo.
pause 