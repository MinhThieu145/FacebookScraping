echo "Installing Python3.9"
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9
python3.9 --version
echo "Python3.9 is installed"
echo "---------------------"
echo "---------------------"
echo "---------------------"
echo "---------------------"
echo "Installing pip3"
sudo apt update
sudo apt install python3-pip
pip3 --version
echo "pip3 installed"