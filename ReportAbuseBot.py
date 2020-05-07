# Import everything.
import praw
import configparser
import sqlite3
import os.path
import time
from pprint import pprint

# Read the configuration.
config = configparser.ConfigParser()
config.read('settings.ini')
reddit_user = config['reportabusebot']['reddit_user']
reddit_pass = config['reportabusebot']['reddit_pass']
reddit_client_id = config['reportabusebot']['reddit_client_id']
reddit_client_secret = config['reportabusebot']['reddit_client_secret']
reddit_target_subreddit = config['reportabusebot']['reddit_target_subreddit']
total_report_threshold = int(config['reportabusebot']['total_report_threshold'])
bot_owner = config['reportabusebot']['bot_owner']
leave_post_comment = config['reportabusebot']['leave_post_comment']

# Create the tracking database.
conn = sqlite3.connect('BotCache.db')
c = conn.cursor()
# id = auto-incrementing value.
# epoch = timestamp.
# postid = the internal Reddit post ID.
# posttitle = the title given to the post by the user.
# redditurl = the link to the post on Reddit.
conn.execute('''CREATE TABLE IF NOT EXISTS reportabusebot
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        epoch INTEGER,
        linkid TEXT,
        posttitle TEXT,
        redditurl TEXT);''')

# Create the Reddit object.
reddit = praw.Reddit(
    username=reddit_user,
    password=reddit_pass,
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent='reportabusebot managed by u/{}'.format(bot_owner)
)

# Start the streaming loop for new submissions.
while True:
  for submission in reddit.subreddit(reddit_target_subreddit).mod.stream.reports():
    try:

      link_id = submission.link_id
      if type(link_id) == type(None):
        continue

      # Insert into the database.
      epoch = time.time()
      c.execute("INSERT INTO reportabusebot (epoch, linkid, redditurl) VALUES (?, ?, ?)", (int(epoch), str(link_id), str(submission.link_permalink)))
      conn.commit()

      # Check and add to the count.
      c.execute("SELECT count() FROM reportabusebot WHERE linkid = ?", (link_id,))
      total_reports = c.fetchone()[0]

      # DEBUG
      print(f'Post ID: {submission.link_permalink}\nTotal Reports: {total_reports}\n')

      # Leave a comment in the thread.

      if total_reports == total_report_threshold and leave_post_comment == 'True':
        print(f'Notice Triggered.\n{submission.link_permalink}\n{submission.link_title}\n')
        comment_text = 'Hello! This is an automated reminder that the report function is not a super-downvote button. Reported comments are manually reviewed and may be removed if they are an actual rule violation. Abuse of the report function is against the site rules and will be reported.\n\nPlease note that I\'m a bot and will not reply.'.format()
        post_submission = reddit.submission(url=submission.link_permalink)
        this_comment = post_submission.reply(comment_text)
        this_comment.mod.distinguish(how='yes', sticky=True)

    except:
      continue

conn.close()
