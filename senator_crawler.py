import tweepy
from tweepy import OAuthHandler
import json
consumer_key = 'aklvl5JcgAI0MjOwRZ6lEZbgC'
consumer_secret = 'to8PgbKDiuhLJMyPwMkw7QjNCG850Kigy9XyybnODIyjReLbt4'
access_token = '3891281112-hgpf7PlWh0HkctcW5ySsGBg8derLC09ANbq17r5'
access_secret = 'DSYcLDlSngGtt9K1G7xIPp3xEyFivERxVpmm2OXvvYSkB'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
user_name = []

#read screen name of 78 senators
with open('data\people.txt', 'r') as f:
    myNames = f.readlines()
#print(myNames[10])
#print(len(myNames))
for i in range(0, len(myNames)):
    user_name.append(myNames[i].strip('\n'))
#print(user_name)
#print(user_name)

temp = open("data\emp.txt", "w")

def process_or_store(tweet):
    temp.write(json.dumps(tweet))
    temp.write('\n')

for i in range(0, len(user_name)):
    for tweet in tweepy.Cursor(api.user_timeline, id=user_name[i]).items():
        process_or_store(tweet._json)


