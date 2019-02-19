@echo off
python -m pip install -r ../requirements.txt
pyinstaller -i ico/udp_icon.ico main.py