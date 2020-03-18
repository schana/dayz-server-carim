SET appdir=.\path\to\dayz-server-carim
SET deploydir=.\path\to\DayZServer\deploy
SET authfile=.\path\to\auth.json
SET outdir=.\path\to\DayZServer
SET logfile=.\path\to\preexec.log
SET "cmd=Python3.exe -m carim.main -d %deploydir% -a %authfile% -o %outdir%"
call :log >>%logfile% 2>&1
exit /b

:log
cd /d %appdir%
git pull
%cmd%
