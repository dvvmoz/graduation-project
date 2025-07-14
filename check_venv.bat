@echo off
echo ========================================
echo Проверка виртуального окружения
echo ========================================

REM Проверяем активацию виртуального окружения
python -c "import sys; assert 'venv' in sys.executable" 2>nul
if errorlevel 1 (
    echo ❌ ОШИБКА: Виртуальное окружение не активировано!
    echo.
    echo Текущий Python: 
    python -c "import sys; print(sys.executable)"
    echo.
    echo Активируйте виртуальное окружение:
    echo venv\Scripts\activate
    echo.
    pause
    exit /b 1
)

echo ✅ Виртуальное окружение активировано!
echo.
echo Информация о среде:
echo - Python: 
python -c "import sys; print(sys.executable)"
echo - Версия: 
python --version
echo - Pip: 
pip --version
echo - VIRTUAL_ENV: %VIRTUAL_ENV%
echo.
echo ========================================
echo Проверка завершена успешно!
echo ======================================== 