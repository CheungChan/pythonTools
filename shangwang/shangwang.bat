@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit
:begin
echo No lockscreen program is running.Please dou't turn off!!!!
cd src
pip install -r requirements.txt
python shangwang.py