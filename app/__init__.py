from flask import Flask

app=Flask(__name__,static_folder='static')
from app import routes
if __name__=='main':

    app.run(debug=True,host='0.0.0.0',port=8081)