#!bin/bash

pip install virtualenv
echo 'Sudo password is required to install python3-venv'
sudo apt install python3-venv
source env/bin/activate

pip install qdrant-client
pip install openai
pip install tqdm
pip install pandas

cd ./docker/
docker compose up
sleep 10s
xdg-open http://example.com

cd ../project/app/
tar -xzf data.tar.gz
python3 app.py