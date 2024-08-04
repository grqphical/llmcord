#! /bin/bash

pyinstaller --noconfirm --onedir --console --name "llmcord" --add-data "./plugins;plugins/" --icon "llmcord_logo.ico" "entry_point.py"