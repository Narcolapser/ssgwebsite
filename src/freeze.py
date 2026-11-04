from flask_frozen import Freezer
from main import app, posts
from pathlib import Path
import shutil

freezer = Freezer(app)

@freezer.register_generator
def get_post():
    for post in posts:
        yield {'post_date': post['date']}

@freezer.register_generator
def get_blog_file():
    for post in posts:
        if post['cover']:
            yield {'post':post['date'],'file_name':'cover.jpg'}
            
        if not post['files']:
            continue
        for file_name in post['files']:
            yield {'post':post['date'],'file_name':file_name}
        

if __name__ == '__main__':
    freezer.freeze()
    destination = Path(app.config['FREEZER_DESTINATION'])
    shutil.copyfile(destination / 'home.html', destination / 'index.html')
