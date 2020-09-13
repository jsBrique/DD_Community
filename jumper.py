#encoding:utf-8
#!/usr/bin/env python
from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import json, requests
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

app.config['DEBUG'] = False
danmu = {}
@app.route('/danmu', methods=['GET'])  # 路由
def danmu_post():



    danmu['str']="哼哼哼啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊"
    danmu['status']=1
    danmu['num']=str(114514)
    return json.dumps(danmu)
@app.route('/')
def index():
    print("有新的dd进入页面")
    return render_template('jump.html')
 

 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4515,debug=False)