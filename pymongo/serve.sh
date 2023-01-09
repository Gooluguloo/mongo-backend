sudo sh ./stop.sh
sudo mongod  --dbpath ./db --fork --logpath /var/log/mongodb/mongod.log
#source ../venv/bin/activate
on_exit()
{
        echo "exiting mongod service...."
        mongopid=$(pgrep mongod)
        echo "the pid for mongod is $mongopid, killing..."
        {
                sudo kill "$mongopid"
                echo "killing process has completed!"
        }||{
                echo "error deleting mongod."
        }
}
#trap on_exit EXIT
flask --app app.py --debug run



