from zeddit import Zeddit
import time
import sys


args = sys.argv
subs = []

for i in range(1, len(args), 2):
    subs.append([args[i], int(args[i+1])])

zobjects = []
for sub in subs:
    zobjects.append(Zeddit(sub[0], sub[1]))

while True:
    for zobject in zobjects:
        posts = zobject.getPosts()
        zobject.sendMultiplePosts(posts)
        zobject.storeToCSV(posts)
        zobject.deleteOldPosts()
    time.sleep(300)
