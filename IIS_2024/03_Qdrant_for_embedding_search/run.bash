#!/bin/bash

pip install virtualenv
echo 'Sudo password is required to install python3-venv'
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate

pip install qdrant-client
pip install openai
pip install tqdm
pip install pandas
pip install requests

cd ./docker/
docker compose up -d  # Run in detached mode

xdg-open http://localhost:6333/dashboard

cd ../project/
python app.py
