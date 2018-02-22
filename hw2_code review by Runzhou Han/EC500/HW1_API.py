# Copyright 2018 Qinjin Jia qjia@bu.edu Github:qinjinjia

# API Library

""" EC500_C1_S'18_HW1_API
File Description and Instruction:
You could use this file as a Library or a Program
If you use this file as a LIBRARY:
there are three functions you could call:
1. get_tweets_imgs_url(screen_name)
   input: screen_name
   output: urls of all images
   description: utilize Twitter API to access the twitter content
2. conv_imgs2video(media_names)
   input: images
   output: a video
   description: utilize FFMPEG to convert images to video
3. describe_imgs(media_names)
   input: images
   output: description of each image
   description: utilize Google Vision analysis to describe the content
If you use this file as a Program
   just type "python HW1_API [screen_name]" in terminal to run
   e.g. python HW1_API @helpanimals
Enjoy and have fun!
"""

"""
Note: To use this library, use 'import HW1_API' in your code.
Additionally, you need to set up a Cloud Platform
Console project and Download a private key as JSON
then, run export GOOGLE_APPLICATION_CREDENTIALS="[PATH]" in terminal.
"""


# Please check my Github @qinjinjia for configuing environment
import os
import io
from sys import argv
import tweepy                        # https://github.com/tweepy/tweepy
import json
import wget
from google.cloud import vision, bigquery
import google.cloud.vision
import subprocess
from shutil import copyfile
import time


start_time = time.time()


# Twitter API credentials
# Please use your own Twitter API credentials here
# Check my Github @qinjinjia for instruction or 
# use Twitter API Link: https://apps.twitter.com
consumer_key = 'DFmJEyJHWEOsF6aJG2dR3nwNd'
consumer_secret = '5ZO9zQz285nHzyC5sN1tT60Y9imbW66pqJHtARO4cA2ZJoHIet'
access_token = '902865296595320832-Cu3uGmxAhpJ72Mk5YKus4hN8PDkbB6e'
access_secret = 'E7i8WMJ9N85927H2cs3Iu4OQJ6zUSDGjJKISbiMfHe6We'
GOOGLE_APPLICATION_CREDENTIALS="Alzheimer's-683341b411e6.json"

    

# Twitter API to Access the Twitter Content
def get_tweets_imgs_url(screen_name = "@llll12431243"):
    "utilize Twitter API to access the twitter content"
    # authorize twitter, initialize tweepy
    @classmethod
    def parse(cls, api, raw):
        status = cls.first_parse(api, raw)
        setattr(status, 'json', json.dumps(raw))
        return status
 
    # Status() is the data model for a tweet
    tweepy.models.Status.first_parse = tweepy.models.Status.parse
    tweepy.models.Status.parse = parse
    # User() is the data model for a user profil
    tweepy.models.User.first_parse = tweepy.models.User.parse
    tweepy.models.User.parse = parse
    # You need to do it for all the models you need
    
    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # Creating an instance, using authentication
    api = tweepy.API(auth)
        
    # initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name, count = 10) # timeout is 60s
    
    # Error handler
    if len(new_tweets) == 0:
        print("The account doesn't exist or Has no tweets.\n")
        return 1

    # save most recent tweets
    alltweets.extend(new_tweets)
    
    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 15):
            break
        print ("...%s tweets downloaded so far" % (len(alltweets)))
       
    # get url for each image
    media_files = set()
    for status in alltweets:
        try:
            media = status.entities.get('media', [])
            if(len(media) > 0):
                media_files.add(media[0]['media_url'])
        except:
            print("An error occurs wilie obtaining image URL.\n")
            return 2

    # download image
    media_names = set()
    for media_file in media_files:
        filename = media_file.split("/")[-1]
        media_names.add(filename)
        wget.download(media_file)
    # show media names
    image_names = []
    image_urls = []
    img_info = {}
    
    new_names = []
    for i in range(len(media_names)):
        new_names.append("image" + str(i))

    for media_file, media_name in zip(media_files, media_names):
        img_name_url = {}
        image_names.append(media_name)
        image_urls.append(media_file)
        print (media_name)
        print (media_file)
        
        img_name_url[media_name] = media_file
        for new_name in new_names:
            img_info[new_name] = img_name_url
    # write image name and url to a json file 
    with open('image_name_and_url.json', 'w') as f:
        json.dump(img_info, f, indent=4)

    return media_names


# FFMPEG to convert images to video
def conv_imgs2video(media_names):
    "utilize FFMPEG to convert images to video" 
    # convert image to video
    try:
        # names for concatenating
        names = open('filenames.txt', 'w')
        for filename in media_names:
            output = filename.replace(".jpg",".mp4")
            names.write("file " + output + "\n")
            cmd = "ffmpeg -loop 1 -i " + filename + " -c:a libfdk_aac -ar 44100 -ac 2 -vf \"scale='if(gt(a,16/9),1280,-1)\':\'if(gt(a,16/9),-1,720)\', pad=1280:720:(ow-iw)/2:(oh-ih)/2\" -c:v libx264 -b:v 10M -pix_fmt yuv420p -r 30 -shortest -avoid_negative_ts make_zero -fflags +genpts -t 1 " + output
            os.system(cmd)
        names.close()
        
        # concate all videos to a video
        concat_cmd = "ffmpeg -f concat -i filenames.txt output.mp4"
        os.system(concat_cmd)
    except:
        print("An error occurs while using FFMPEG.\n")
        return 3
    

# Google Vision analysis to describe the content
def describe_imgs(media_names):
    "utilize Google Vision analysis to describe the content"
    # Create a Vision client.
    vision_client = google.cloud.vision.ImageAnnotatorClient()
    
    img_descrip = {}
    
    # file to analyze.
    for image_file_name in media_names:
        with io.open(image_file_name, 'rb') as image_file:
            content = image_file.read()

        # Use Vision to label the image based on content.
        image = google.cloud.vision.types.Image(content=content)
        response = vision_client.label_detection(image=image)

        image_desc = []

        for label in response.label_annotations:
            features = {}
            features['mid'] = label.mid
            features['description'] = label.description 
            features['score'] = str(label.score)
            features['topicality'] = str(label.topicality)
            image_desc.append(features)

        img_descrip[image_file_name] = image_desc

    with open('image_description.json','w') as f:
        json.dump(img_descrip, f, indent = 4)

def main():
    "use this file as a Program"
    # The defulat scrren_name is "@helpanimals"
    try:
        if len(argv) == 2:
            screen_name = argv[1]
        else:
            screen_name = "@helpanimals"
            media_names = get_tweets_imgs_url(screen_name)
            print("--- %s seconds ---" % (time.time() - start_time))    
            conv_imgs2video(media_names)  
            print ("Time for cinverting images to vedio" , time.time() - start_time, "seconds")
            describe_imgs(media_names)
            print("--- %s seconds ---" % (time.time() - start_time))
    except:
        pass
#    print("***************************************")
#    print("Congratulation!\n")
#    print("There are " + str(len(media_names)) + " images downloaded from " + screen_name + "\n")
#    print("image_name_and_url.json (Twitter API to access the twitter content)\n")
#    print("output.mp4 (FFMPEG to convert images to video)\n")
#    print("image_description.json (Google Vision analysis to describe the content)\n")
#    print("***************************************")


# for using this file as a Library
if __name__ == '__main__':
    main()