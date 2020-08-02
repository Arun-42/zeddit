import configparser
import pandas as pd
import time
import praw
import zulip
import os

class Zeddit:

    def __init__(self, subName, upvoteThreshold):
        # create file if not
        self.getRedditCredentials()
        self.subName = subName
        self.getSub(subName)
        self.upvoteThreshold = upvoteThreshold
        self.createFileIfNonExistent()

    def createFileIfNonExistent(self):
        if not os.path.exists(self.getFileName()):
            with open(f'{self.getFileName()}', 'w+') as file:
                file.write('id,time')

    def getFileName(self):
        return f'{self.subName}.csv'

    def getSub(self, subName):
        self.subReddit = praw.Reddit(
            client_id=self.clientId, 
            client_secret=self.clientSecret, 
            user_agent=self.userAgent
        ).subreddit(subName)

    def getRedditCredentials(self):
        config_file = configparser.RawConfigParser()
        config_file.read("auth_info.conf")
        auth_info = config_file['auth']

        self.clientId = auth_info.get("id")
        self.clientSecret = auth_info.get("secret")
        self.userAgent = auth_info.get("ua")
    
    def isDuplicate(self, post_id):
        df = pd.read_csv(self.getFileName())
        if post_id in set(df.id):
            return True
        return False

    def getPosts(self):
        posts = self.subReddit.top("day")
        unique_posts = []
        for post in posts:
            if post.score >= self.upvoteThreshold:
                if not self.isDuplicate(post_id=post.id):
                    unique_posts.append(post)
            else:
                break
        return unique_posts

    def storeToCSV(self, posts):
        data=[]
        for post in posts:
            data.append([post.id, time.time()])
        df = pd.DataFrame(data, columns=["id", "time"])
        df.to_csv(self.getFileName(), mode = "a", header=False)

    def deleteOldPosts(self, file_name=None):
        twoDaysInSeconds = 2*24*60*60
        timeNow = int(time.time())
        timeTwoDaysAgo = timeNow - twoDaysInSeconds
        if file_name is None:
            file_name = self.getFileName()
        df = pd.read_csv(file_name)
        df = df.drop(df[df.time < timeTwoDaysAgo].index)

    def getZulipClient(self):
        return zulip.Client(config_file="./zuliprc")

    def sendToZulip(self, post):
        post_title = post.title
        post_url = post.url

        message_body = "" + post_title + "" + '\n' + post_url
        message = {
            "type": "stream",
            "to": "Reddit",
            "topic": self.subName,
            "content": message_body,
        }
        zulip_client = self.getZulipClient()
        result = zulip_client.send_message(message)
        return result

    def sendMultiplePosts(self, posts):
        for post in posts:
            self.sendToZulip(post)
        numberOfPosts = len(posts)       
        print("Number of posts made:", numberOfPosts)
