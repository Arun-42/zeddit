from zeddit import Zeddit
import sys

def getSubReddit(args):
    # We expect the subreddit to be first argument
    return args[1]

def getUpvoteThreshold(args):
    # We expect the upvotes threshold to be second argument
    return int(args[2])

args = sys.argv
if(len(args) <=2 ):
    print("Pass proper arguments. Subreddit name first, upvotes next")

subreddit = getSubReddit(args)
upvoteThreshold = getUpvoteThreshold(args)

zobject = Zeddit(subreddit, upvoteThreshold)
posts = zobject.getPosts()
zobject.sendMultiplePosts(posts)
zobject.storeToCSV(posts)
