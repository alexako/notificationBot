import praw
import config
from pprint import pprint

class RedditBot():
    """
        Initialize the bot with the following parameters
        Parameters: bot_name, version, user_name
        E.g. RedditBot("Test bot", "0.1", "/u/gallowboob")
    """

    def __init__(self, bot_name, version, user_name):
        user_agent = "%s %s by /u/%s" % (bot_name, version, user_name)
        self.r = praw.Reddit( client_id=config.CLIENT_ID,
                        client_secret=config.CLIENT_SECRET,
                        user_agent=user_agent,
                        username=config.USERNAME,
                        password=config.PASSWORD)
        self.user = self.r.redditor(user_name)

    def get_submitted(self, limit=None):
        """Returns submissions from this bot"""
        return [post for post in self.user.submissions.new(limit=limit)]

    def get_comments_by_bot(self, limit=None):
        """Returns comments from this bot"""
        return [comment for comment in self.user.comments.new(limit=limit)]
    
    def get_subreddit(self, subreddit="all"):
        """ Returns subreddit object """
        return self.r.subreddit(subreddit)

    def get_submissions(self, subreddit="all", limit=10):
        """
            Returns submissions list from given subreddit [default top 10 posts from hot list]
            Parameters: subreddits="all", limit=10
            Multisubreddits => all+funny+AMA
        """
        return [submission for submission in self.r.subreddit(subreddit).hot(limit=limit)]

    def get_comments(self, submission, query=""):
        """Returns a list of comments [PRAW object] from a given submission [PRAW object]"""
        comments = submission.comments[:-1]
        return [comment for comment in comments if query.lower() in comment.body.lower()]

    def reply_to_comment(self, comment, response="Hello"):
        try:
            comment.reply(response)
        except:
            print("ERROR: Replay not posted")
            exit(1)

    def print_submission(self, submission):
        pprint(submission)


if __name__ == '__main__':

    #Instantiate
    bot = RedditBot("test bot", "0.1", "/u/kludgebot")

    #Get submissions from subreddit [default=/all]
    sub_query = input("Enter thread to search: ")
    print("Searching reddit for /r/%s..." % sub_query)
    submissions_all = bot.get_subreddit(sub_query)

    print()

    #Print top submission 
    sub_author = submissions_all[0].author
    sub_title = submissions_all[0].title
    print("Title:", sub_title)
    print("OP:", sub_author)

    #Print first comment from top submission
    print("Best comment:", submissions_all[0].comments[0].body)

    #Query comments from top submission
    query = input("Enter query: ")
    print("Searching comments for '%s' in /r/%s/%s..." % (query, sub_query, sub_title))
    r = bot.get_comments(submissions_all[0], query)
    result = r if len(r) > 0 else ["No results found"]
    print("===========================================")
    print("Results found: %d" % len(r) if r[0] != "No results found" else 0)
    for index, comment in enumerate(result):
        print("%d) Author: %s\n%s\n" % (index+1, comment.author, comment.body))
