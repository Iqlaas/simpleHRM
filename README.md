# Simple HRM

git clone

cd simpleHRM/

python3 -m venv env   #create a virtual environment

source env/bin/activate  #activate your virtual environment

pip3 install -r requirements.txt

uvicorn app:app --reload     #start server

visit  127.0.0.1:8000/docs