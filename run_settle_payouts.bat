@echo off

REM Activate virtual environment
call D:\Yasla Saloon App\env\Scripts\activate.bat

REM Change directory to the Django project root (where manage.py is located)
cd /d D:\Yasla Saloon App\Yasla\Yasla

REM Run the Django management command
python manage.py settle_vendor_payouts --force >> "D:\Yasla Saloon App\Yasla\Yasla\logs\settle_payouts.log" 2>&1

REM Pause to keep the window open (optional for debugging)
pause
