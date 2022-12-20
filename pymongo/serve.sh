sudo mongod  --dbpath ./db --fork --logpath /var/log/mongodb/mongod.log
source ../venv/bin/activate
flask --app app.py --debug run
