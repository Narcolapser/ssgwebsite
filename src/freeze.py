from flask_frozen import Freezer
from main import app
import os
import shutil

from datetime import datetime

freezer = Freezer(app)

def is_date(val):
    try:
        datetime.strptime(val,'%Y-%m-%d')
        return True
    except:
        return False



@freezer.register_generator
def get_post():
    posts = [{'date':post} for post in os.listdir('/home/toby/Code/ssg-blog') if is_date(post)]
    for post in posts:
        yield {'post_date': post['date']}

if __name__ == '__main__':
    freezer.freeze()
    shutil.copyfile('./dist/home.html','./dist/index.html')