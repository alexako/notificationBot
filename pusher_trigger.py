from pusher import Pusher
import config

class Trigger():
    def __init__(self, bot, event):
        self.bot = bot
        self.event = event
        self.pusher = Pusher(
                app_id=config.APP_ID,
                key=config.KEY,
                secret=config.SECRET)

    def push(self, content):
        self.pusher.trigger(
                self.bot,
                self.event,
                { u'content' : content }
            )

if __name__ == '__main__':
    trigger = Trigger("my-channel", "my-event")
    trigger.push("Hello world")