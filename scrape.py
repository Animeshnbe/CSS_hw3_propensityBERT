import pprint
import json
import praw
import sys
reddit_ro = praw.Reddit(client_id="NfS5P4Nd-35O7IJgZj4HmQ",         # your client id
                        client_secret="5rM1kcEraAx7ewuvoy46oIlQuN5Frw",      # your client secret
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46")        # your user agent




def append_to_json(_dict, sub):
    with open("posts_"+sub+".json", 'ab+') as f:
        f.seek(0, 2)  # Go to the end of file
        if f.tell() == 0:  # Check if file is empty
            f.write(json.dumps([_dict]).encode())  # If empty, write an array
        else:
            f.seek(-1, 2)
            f.truncate()  # Remove the last character, open the array
            f.write(' , '.encode())  # Write the separator
            f.write(json.dumps(_dict).encode())  # Dump the dictionary
            f.write(']'.encode())


'''
    pass the count param to the scrape posts function if you need to scrape more posts
    currently in dfs, takes ~1.4s per post with ~25 comments each on average
'''


def scrape_posts(subreddit, count=1000):
    print("Scraping subreddit: ", subreddit.display_name)
    sys.stdout.flush()
    posts = subreddit.top(time_filter="all")
    # Scraping the top posts of the current month

    # from praw.models import MoreComments
    if count:
        c = 0

    for post in posts:
        # if post.media_only:
        print(post.title)
        sys.stdout.flush()
        # pprint.pprint(vars(post))

        if c > count:
            break

        if post.num_comments > 3:
            posts_dict = {}
            posts_dict["title"] = post.title
            posts_dict["text"] = post.selftext
            posts_dict["id"] = post.id
            posts_dict["score"] = post.score
            posts_dict["total_comments"] = post.num_comments
            if post.author:
                posts_dict["author"] = post.author.name
            else:
                posts_dict["author"] = ""
            posts_dict["url"] = post.url
            posts_dict["created"] = post.created_utc
            posts_dict["upvote_ratio"] = post.upvote_ratio
            posts_dict["score"] = post.score
            post_comments = []
            post.comments.replace_more(limit=None)
            comment_queue = post.comments[:]
            while comment_queue:
                comment = comment_queue.pop(0)
                if comment.body.startswith('[') or comment.body.startswith('/r'):
                    continue
                if comment.author:
                    post_comments.append({comment.author.name: comment.body})
                else:
                    post_comments.append({"anonymous": comment.body})
                comment_queue[0:0] = comment.replies
            posts_dict["comments"] = post_comments
            append_to_json(posts_dict, sub)
            c += 1
            # break


subreddits = ["wholesomememes", "politicalhumor", "memes", "askreddit",
              "music", 'aww', 'worldnews', 'movies', 'pics', "mademesmile"]
for sub in subreddits:
    print("Scraping subreddit: ", sub)
    sr = reddit_ro.subreddit(sub)
    scrape_posts(sr)
# Saving the data in a pandas dataframe
# top_posts = pd.DataFrame(posts_dict)
# top_posts
