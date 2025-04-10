from flask import Flask, render_template, request, send_file
import os
from pathlib import Path
import json
import markdown2
from datetime import datetime

def is_date(val):
    try:
        datetime.strptime(val,'%Y-%m-%d')
        return True
    except:
        return False

app = Flask(__name__)
app.config['FREEZER_DESTINATION'] = '../dist'

ssg_blog_path = '/home/toby/Code/ssg-blog'
#ssg_blog_path = '/Users/toby/Code/ssg-blog'

posts = [{'date':post} for post in os.listdir(ssg_blog_path) if is_date(post)]
posts = sorted(posts, key=lambda x: x['date'], reverse=True)
all_tags = set()
for post in posts:
    post['content'] = open(f'{ssg_blog_path}/{post["date"]}/post.md').read()
    info = json.load(open(f'{ssg_blog_path}/{post["date"]}/info.json'))
    post['title'] = info['title']
    post['tags'] = info['tags']
    post['files'] = info['files'] if 'files' in info else None
    cover_path = Path(f'{ssg_blog_path}/{post["date"]}/cover.jpg')
    post['cover'] = cover_path.exists()
    all_tags.update(info['tags'])

post_dict = {post['date']:post for post in posts}

print(all_tags)

@app.route('/index.html')
@app.route('/home.html')
#@app.route('/')
def root():
    post = posts[0]
    post['content_html'] = markdown2.markdown(post['content'])
    return render_template('index.html', post=post)

@app.route('/static/<file_name>')
def get_resource(file_name):
    print(file_name)
    return send_file("static/" + file_name)

@app.route('/static/<post>/<file_name>')
def get_blog_file(post, file_name):
    print(file_name)
    print(post)

    if post == 'font':
        return send_file(f'static/font/{file_name}')
    elif post == 'homestead':
        return send_file(f'static/homestead/{file_name}')
    else:
        return send_file(f'{ssg_blog_path}/{post}/{file_name}')

@app.route('/post.html')
def get_posts():
    return render_template('posts.html',posts=posts)

@app.route('/post/<post_date>.html')
def get_post(post_date):
    post = post_dict[post_date]
    post['content_html'] = markdown2.markdown(post['content'])
    return render_template('post.html',post=post_dict[post_date])

@app.route('/tag.html')
def get_tags():
    tag_collections = {}
    for tag in all_tags:
        tag_collections[tag] = []
    
    for post in posts:
        for tag in post['tags']:
            tag_collections[tag].append({'date':post['date'], 'title': post['title']})
                
    return render_template('tags.html',tags=tag_collections)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
