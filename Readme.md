# Subtitling of BBB Participants
This project is to subtitle BBB participants each induvidually.

## Installation:
Requirements:
Works with BigBlueButton 2.2.x and Ubuntu 16.04
Working kaldi-model-server
At first create a directory and clone the projects into it:
```Shell
mkdir ~/projects
cd ~/projects
git clone https://www.github.com/alienmaster/BA-Programs
```
Create kaldi-model-server and follow the [instructions](https://github.com/uhh-lt/kaldi-model-server#installation)

After these steps create a virtual enviroment and start it
```Shell
cd ~/projects/BA-Programs
virtualenv -p python3 bbb_env
source bbb_env/bin/activate
```
Install the dependencies
```Shell
pip3 install redis
```

## Usage
To use this project you can run every script on independent machines or all on the same.
All the scripts need to run before the participant joins the conference.
At first you need to start `esl_to_redis.py`. This module creates a connection to the freeswitch Software and writes every information about the media bugs into the redis channel.
The next to start is `check_redis_and_start_upload.py`. This module checks the redis channel for information and starts the file upload onto the asr channel.
The `kaldi_starter.py` module is in my configuration on another machine and starts for every participant an own kaldi instance.
With the `mongodbconnector.py` module the ASR Data is send into the mongodb database and is visible for the participants.