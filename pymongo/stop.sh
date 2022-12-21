mongopid=$(pgrep mongod)
if [ -z "$mongopid" ]
then
        echo "mongod does not exist."
else
                     
        echo "The pid for mongod is $mongopid, killing..."
        sudo kill "$mongopid"
fi

flaskpid=$(pgrep flask)
if [ -z "$flaskpid" ]
then
        echo "flask does not exist."
         
else
                     
        echo "The pid for flask is $flaskpid, killing..."
        sudo kill "$flaskpid"
        

fi
 
