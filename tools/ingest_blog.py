"""
This script is responsible for taking my existing content in my blog repository and converting it into a format that Pelican likes. 

All the published posts are in folders with dates for names containing a post.md, info.json, and cover.jpg(or png?).
"""

import os
import json
from datetime import datetime

def is_date(val):
    try:
        datetime.strptime(val,'%Y-%m-%d')
        return True
    except:
        return False

posts = [post for post in os.listdir('/Users/toby/Code/ssg-blog') if is_date(post)]

for post in posts:
    content = open(f'/Users/toby/Code/ssg-blog/{post}/post.md').read()
    info = json.load(open(f'/Users/toby/Code/ssg-blog/{post}/info.json'))
    title = info['title']
    date = post
    tags = ', '.join(info['tags'])

    new_post = f'Title: {title}\nDate: {date}\nTags: {tags}\n\n{content}'

    outs = open(f'../src/content/Blog/{post}.md','w')
    outs.write(new_post)
    outs.close()
