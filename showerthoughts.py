from zeddit import Zeddit
import time

zobject = Zeddit('showerthoughts', 1000)
while True:
    posts = zobject.getPosts()
    zobject.sendMultiplePosts(posts)
    zobject.storeToCSV(posts)
    time.sleep(300)
