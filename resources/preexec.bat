SET appdir=.\path\to\dayz-server-carim
SET deploydir=.\path\to\DayZServer\deploy
SET authfile=.\path\to\auth.json
SET outdir=.\path\to\DayZServer
for /f %%i in ('powershell -c "get-date -format yyyy-MM-dd-HHmmss"') do @set datetime=%%i
SET logfile=.\path\to\preexec_%datetime%.log
SET "cmd=Python3.exe -m carim.main -d %deploydir% -a %authfile% -o %outdir%"
call :log >>%logfile% 2>&1
exit /b

:log
cd /d %appdir%
git pull
%cmd%
