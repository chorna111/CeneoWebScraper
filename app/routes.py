from app import app
@app.route('/')
@app.route('/index')
def index():
    return 'Hello, Anastazja Czorna!'
@app.route('/name/',defaults={'name':None})
@app.route('/name/<name>')
def name(name):
    return f'Hello,{name}!'


