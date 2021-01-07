# Subtitling of BBB Participants
This project is to subtitle BBB participants each induvidually.

## Installation:
Requirements:
Works with BigBlueButton 2.2.x and Ubuntu 16.04

At first create a directory and clone the projects into it:
```Shell
mkdir ~/projects
cd ~/projects
git clone https://www.github.com/alienmaster/BA-Programs
cd BA-Programs
git clone https://github.com/Alienmaster/kaldi-model-server
git clone https://github.com/pykaldi/pykaldi
```
Create a virtual enviroment and start it
```Shell
virtualenv -p python3 bbb_env
source bbb_env/bin/activate
```
Install the dependencies
```Shell
pip install numpy pyparsing ninja redis pyyaml pyaudio flask flask_cors bs4 samplerate scipy
```

Compile and install Protobuf, CLIF and KALDI dependencies (compiliation can take some time unfortunatly):
```Shell
cd  ~/projects/BA-Programs/pykaldi/tools/
./check_dependencies.sh  # checks if system dependencies are installed
./install_protobuf.sh ~/projects/BA-Programs/bbb_env/bin/python3  # installs both the Protobuf C++ library and the Python package
./install_clif.sh ~/projects/BA-Programs/bbb_env/bin/python3  # installs both the CLIF C++ library and the Python package
./install_kaldi.sh ~/projects/BA-Programs/bbb_env/bin/python3 # installs the Kaldi C++ library