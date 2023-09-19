from flask import Flask, render_template, request, send_file
import os
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

posts = [{'date':post} for post in os.listdir('/home/toby/Code/ssg-blog') if is_date(post)]
posts = sorted(posts, key=lambda x: x['date'], reverse=True)
all_tags = set()
for post in posts:
    post['content'] = open(f'/home/toby/Code/ssg-blog/{post["date"]}/post.md').read()
    info = json.load(open(f'/home/toby/Code/ssg-blog/{post["date"]}/info.json'))
    post['title'] = info['title']
    post['tags'] = info['tags']
    all_tags.update(info['tags'])

post_dict = {post['date']:post for post in posts}

print(all_tags)

@app.route('/index.html')
@app.route('/home.html')
def root():
    return render_template('index.html')

@app.route('/static/<file_name>')
def get_resource(file_name):
    print(file_name)
    return send_file("static/" + file_name)

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
