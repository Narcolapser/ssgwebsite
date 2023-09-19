from flask import Flask, render_template, request, send_file

app = Flask(__name__)
app.config['FREEZER_DESTINATION'] = '../dist'

@app.route('/')
def root():
    return 'hello world'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)