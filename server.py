#encoding:utf-8
#!/usr/bin/env python
from flask import Flask, render_template,request
from flask_socketio import SocketIO
from analyse import analyse
import random
import json, requests
import time
import sys
import curses
import redis
import os
import threading
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

#socketio = SocketIO(app)


user_ip={}
lasttime = time.time()
rd = redis.StrictRedis(host='localhost', port=4514, db=0,decode_responses=True)
lastk=[]
status=requests.get('https://api.live.bilibili.com/room/v1/Room/room_init?id=801580').json()
top,hantalk=analyse()
lastsize=0
# limiter.init_app(app)
today_danmu=""
def main_server():
    #socketio.run(app, host='0.0.0.0', port=14514,debug=False)
    app.run( host='0.0.0.0', port=14514,debug=False,threaded=True)
def reflash_today():
    global today,today_danmu,status,lasttime,user_ip,lastsize
    while True:
        today=time.strftime("%Y-%m-%d", time.localtime())
        status=requests.get('https://api.live.bilibili.com/room/v1/Room/room_init?id=801580').json()
        flash_lock.acquire()
        now_time=time.time()
        if(now_time - lasttime > 300):
            user_ip={}
            lasttime=now_time
        reflashflag=False
        nowsize=rd.dbsize()
        if len(user_ip)>0 and (nowsize!=lastsize  or status['data']['live_status']==1)  :
            today_danmu=search_danmu(today,True)
            reflashflag=True
            lastsize=nowsize
        
        flash_lock.release()
        
        #print(status['data'])
        top,hantalk=analyse()
        os.system("clear")
        board="当前在线dd：\n"
        for iip in user_ip:
            board = board +' '+str(iip)+ ' '+str(user_ip[iip]['cname'])+' '+str(user_ip[iip]['date'])+user_ip[iip]['mode']+'\n'
        print(board)
        print('\n常规更新 数据库变动:',reflashflag,'开播模式:',status['data']['live_status'],'更新时间',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if status['data']['live_status']==1 :
            time.sleep(6)
        elif reflashflag==True:
            time.sleep(9)
        else:
            time.sleep(19)

flash_td=threading.Thread(target=reflash_today)
main_server_td=threading.Thread(target=main_server)
flash_lock=threading.Lock()
today=time.strftime("%Y-%m-%d", time.localtime())



def search_danmu(date,reflash=False):
    if date==today and reflash==False:
        # print('\n快速查询')
        return get_today()
    else:
        # if reflash==False:
        #     print('\n慢速查询',date,today)
        # if reflash==True:
        #     print('\n常规更新',date,today)
        ks=rd.keys('*'+str(date)+'*')
        datares={}
        for k in ks:
            e=k.find('T')
            ind=int(k[0:e])
            datares[ind]=rd.hgetall(k)
        dataout = sorted(datares.items(), key=lambda d:d[0], reverse = False)
        danmu_str=""
        for l in dataout:
            danmu_str=str(l[1]['time']+' '+l[1]['name']+': <br>'+l[1]['text'])+"<br>" + danmu_str
        return danmu_str

def get_today():
    global today_danmu
    return today_danmu
@app.route('/danmu', methods=['GET'])  # 路由
# @limiter.limit('30/minute')
def danmu_post():
    global user_ip
    
    danmu = {}

    danmu['top'],danmu['hantalk']=top,hantalk
    
    ip =  request.args.get("ip")
    cname =  request.args.get("cname")
    date =  request.args.get("searchdate")
    if date==today:
        searchmode=" 快查"
    else:
        searchmode=" 慢查"
    flash_lock.acquire()
    user_ip[ip]={'cname':cname,'date':date,'mode':searchmode}
    st=search_danmu(date)
    flash_lock.release()
    danmu['str']=st
    danmu['status']=status['data']['live_status']
    danmu['num']=str(len(user_ip))
    
    time.sleep(0.1)
    return json.dumps(danmu)

@app.route('/dd')
def dd():
    return render_template('dd2.html')
@app.route('/')
def index():


    return render_template('index.html')
 

 
def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list




if __name__ == '__main__':
    flash_td.start()
    main_server_td.start()
    flash_td.join()
    main_server_td.join()

    