import datetime
import re
import sys
from time import sleep, strftime, localtime
import praw
import redditBot
from pusher_trigger import Trigger


class NotificationBot:

    def __init__(self, botName, version, author, subreddit, trigger):
        self.bot = redditBot.RedditBot(botName, version, author)
        self.botName = botName
        self.subreddit = self.bot.get_subreddit(subreddit)
        self.trigger = trigger
        self.retries = 0
        self.startTime = datetime.datetime.now()
        self.pusher = Trigger(self.botName, "triggered")

    def convertDateTime(self, epoch):
        return datetime.datetime.fromtimestamp(epoch)

    def convertDateTimeString(self, epoch):
        return strftime('%Y-%m-%d %H:%M:%S', localtime(epoch))

    def isRecent(self, comment):
        comment_date = self.convertDateTime(comment.created_utc)
        comment_date = comment_date + datetime.timedelta(minutes=30)
        return comment_date > self.startTime
    
    def trigger_event(self, comment):
        payload = {
            'author': comment.author.name,
            'body': comment.body,
            'date': self.convertDateTimeString(comment.created_utc),
            'link': comment.submission.shortlink
        }

        print(payload)

        try:
            self.pusher.push(payload)
            print("Triggered! %s"
                % (str(datetime.datetime.now()).split('.')[0]))
        except Exception as e:
            print(e)


    def listen(self):
        print("Started listening for %s in /r/%s at %s..."
            % (self.trigger, self.subreddit.display_name, str(self.startTime).split('.')[0]))
        try:
            for comment in self.subreddit.stream.comments():
                if self.trigger in comment.body:
                    try: self.trigger_event(comment)
                    except: continue

        except praw.exceptions.APIException as e:
            if e.error_type == "RATELIMIT":
                print(e.message)

                if re.match("(\d+) minutes?", e.message):
                    delay = re.search("(\d+) minutes?", e.message)
                    delay_seconds = float(int(delay.group(2)) * 60)
                else:
                    delay = re.search("(\d+) seconds", e.message)
                    delay_seconds = float(int(delay.group(1)))

                sleep(delay_seconds)
                self.listen()
        except:
            self.retries += 1
            if self.retries > 5:
                print("Maximum retries attempted")
                exit(1)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: python notificationBot.py [SUBREDDIT] [TRIGGER WORD]")
        exit(1)

    subreddit = sys.argv[1]
    trigger = sys.argv[2]

    n = NotificationBot("NotificationBot",
                        "0.1",
                        "/u/kludgebot",
                        subreddit,
                        trigger)
    
    n.listen()