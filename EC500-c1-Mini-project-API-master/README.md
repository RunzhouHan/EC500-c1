# EC500-c1-Mini-project-API
## Basic information
Author: Runzhou Han

E-mail: rzhan@bu.edu

BU ID: U81215139

## Project discription
Twitter API to access the twitter content

FFMPEG to convert images to videos

Google Vision analysis to describe the content 

## Implementation

### Preparation

First, we'll make a workspace:

cd ~

mkdir gcloudstuff

cd gcloudstuff

sudo apt-get install python-pip

Now we can install the Google Cloud API stuff:

sudo pip install google-cloud

This will install all of the APIs.You can also do specific APIs, like sudo pip install google-cloud-vision for example for vision.

Next, we need to to setup the API credentials. To do this, open the side bar by clicking on the hamburger icon, and then choose the API manager, then go to Credentials on the side.

Now choose to create credentials > choose "service account key" > choose new service account > Make a name > select a role. I personally chose project > owner, so we had full access, but you can make specific keys for specific people if you would like. Now hit create, and this will return to you a json file of your key information. Open up this .json file, and copy the contents. Now head back to the server shell, and do nano apikey.json to open up a new file in the shell, and paste in the json contents. Different shells will act differently, some will support control+c and control+v, others will copy and paste with a right click, others can be right click copied and pasted. To leave nano, control+x to leave, y to save it, and you're all set.

### Demo
 ![Main page](https://raw.github.com/RunzhouHan/EC500-c1/blob/EC500-c1-Mini-project-API-master/master/Commandline1.png)
 ![Main page](https://raw.github.com/RunzhouHan/EC500-c1/blob/master/EC500-c1-Mini-project-API-master/Commandline2.png)
 ![Main page](https://raw.github.com/RunzhouHan/EC500-c1/blob/master/EC500-c1-Mini-project-API-master/Labels.png)




