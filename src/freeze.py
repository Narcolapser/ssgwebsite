from flask_frozen import Freezer
from main import app
import os
import shutil
import json
from datetime import datetime

freezer = Freezer(app)

ssg_blog_path = '/home/toby/Code/ssg-blog'
ssg_blog_path = '/Users/toby/Code/ssg-blog'

def is_date(val):
    try:
        datetime.strptime(val,'%Y-%m-%d')
        return True
    except:
        return False

posts = [{'date':post} for post in os.listdir(f'{ssg_blog_path}') if is_date(post)]
posts = sorted(posts, key=lambda x: x['date'], reverse=True)
all_tags = set()
for post in posts:
    #post['content'] = open(f'/home/toby/Code/ssg-blog/{post["date"]}/post.md').read()
    info = json.load(open(f'{ssg_blog_path}/{post["date"]}/info.json'))
    post['title'] = info['title']
    post['tags'] = info['tags']
    post['files'] = info['files'] if 'files' in info else None
    all_tags.update(info['tags'])

post_dict = {post['date']:post for post in posts}

@freezer.register_generator
def get_post():
    for post in posts:
        yield {'post_date': post['date']}

# @app.route('/static/<post>/<file_name>')
# def get_blog_file(post, file_name):
@freezer.register_generator
def get_blog_file():
    for post in posts:
        print(post)
        if not post['files']:
            continue
        for file_name in post['files']:
            yield {'post':post['date'],'file_name':file_name}

if __name__ == '__main__':
    freezer.freeze()
    shutil.copyfile('./dist/home.html','./dist/index.html')
