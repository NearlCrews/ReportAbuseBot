# ReportAbuseBot
A PRAW bot for reminding people not to abuse the report function.

# Summary
People like to use the report function as a super-downvote button. This bot simply posts a message in the channel to remind everyone that the report button is for actual rule violation. It reads the report stream, keeps a total on the number of reports, and then leaves the message when it crosses a defined threshold.

# Installation
Install the required modules:
```
pip3 install --upgrade configparser praw
```

You want to plug the correct values into `settings.ini`. They're fairly simple:
```
[reportabusebot]
# Bot username and password, or use your own.
reddit_user =
reddit_pass =
# Create the secret OATH values. Instructions on Reddit.
reddit_client_id =
reddit_client_secret =
# Subreddit to monitor, e.g. Michigan.
reddit_target_subreddit =
# Total number of comment reports before the notice is posted.
total_report_threshold = 4
# Bot owner. This is typically your username. Don't add the u/ in front of the name.
bot_owner =
# Set to true if you'd like the bot to leave a comment on the post.
leave_post_comment = True
```

You then simply run the bot:
`python3 ReportAbuseBot.py`

I run it in `screen` since I'm ususlly watching the ouput. It'll also write the processed events to a local database so it's not sending repeat alerts if it needs to reprocess. 

**Sample Message:**

```
Hello! This is an automated reminder that the report function is not a super-downvote button. Reported comments are manually reviewed and may be removed if they are an actual rule violation. Abuse of the report function is against the site rules and will be reported.

Please note that I'm a bot and will not reply.
```
