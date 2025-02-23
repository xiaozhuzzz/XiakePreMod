@echo off
chcp 65001


for %%f in (*.txt) do (
	echo Converting "%%f" to UTF-8...
	type "%%f" > "%%~nf.tmp"
	move /y "%%~nf.tmp" "%%~nf.txt"
)

pause	