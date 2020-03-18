SET appdir=.\path\to\dayz-server-carim
SET deploydir=.\path\to\DayZServer\deploy
SET authfile=.\path\to\auth.json
SET outdir=.\path\to\DayZServer
SET "cmd=Python3.exe -m carim.main -d %deploydir% -a %authfile% -o %outdir%"

start /d %appdir% cmd /k "%cmd% && exit"
