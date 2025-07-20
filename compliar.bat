@echo off
cd /d "%~dp0"
pyinstaller --onefile --noconsole ^
--add-data "C:\Users\beto_\AppData\Local\Programs\Python\Python313\Lib\site-packages\mysql\connector\locales;mysql\connector\locales" ^
--add-data "C:\Users\beto_\AppData\Local\Programs\Python\Python313\Lib\site-packages\mysql\connector\plugins;mysql\connector\plugins" ^
main.py
pause
