from zeddit import Zeddit
import time
import sys

subreddit = sys.argv[1]
upvote_threshold = int(sys.argv[2])

zobject = Zeddit(subreddit, upvote_threshold)
while True:
    posts = zobject.getPosts()
    zobject.sendMultiplePosts(posts)
    zobject.storeToCSV(posts)
    zobject.deleteOldPosts()
    time.sleep(300)
