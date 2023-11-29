# More Data
from pmaw import PushshiftAPI
api = PushshiftAPI()
import datetime as dt
after = int(dt.datetime(2022,1,1,0,0).timestamp())
before = int(dt.datetime(2022,12,31,0,0).timestamp())

subreddit="mademesmile"
# limit=150
comments = api.search_comments(subreddit=subreddit, limit=None, before=before, after=after, include_removed=True)
print(f'Retrieved {len(comments)} comments from Pushshift')

import pandas as pd
df = pd.DataFrame(columns=["author", "comment"])
comment_data = []
# iterate over the fetched comments and append the author and comment to the DataFrame
for comment in comments:
    # if comment['body']=='[removed]':
        
    print(comment["body"])
    if comment['author']=='[deleted]':
        comment_data.append({
            "author": "anonymous",
            "comment": comment['body']
        })
    else:
        comment_data.append({
            "author": comment['author_fullname'][3:],
            "comment": comment['body']
        })

# create a DataFrame from the comment data
df = pd.DataFrame(comment_data, columns=["author", "comment"])

df.to_csv('comments1.csv', index=False)