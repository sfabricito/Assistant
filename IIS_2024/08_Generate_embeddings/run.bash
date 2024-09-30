#!/bin/bash

pip install virtualenv
echo 'Sudo password is required to install python3-venv'
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

python app.py