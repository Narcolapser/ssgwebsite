from flask import Flask, render_template, request, send_file

app = Flask(__name__)
app.config['FREEZER_DESTINATION'] = '../dist'

@app.route('/')
def root():
    return render_template('index.html')

@app.route("/static/<file_name>")
def get_resource(file_name):
    print(file_name)
    return send_file("static/" + file_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
