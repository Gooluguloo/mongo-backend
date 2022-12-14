echo "Setting up enviroment for Gooluguloo..."

pip install virtualenv

if [ ! -d "./venv" ]; then
    echo "Creating virtual environment..."
    sudo python -m venv venv
fi

source ./venv/bin/activate
pip install -r requirements.txt

if [ ! -f "./.env" ]; then
    echo "Creating env file..."
    touch ./.env
fi
mkdir ./instance/
touch ./instance/test.db
echo "Setup complete. Please run serve.bash to start the backend server."
