#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request, render_template
from selenium import webdriver
import pymysql.cursors
import ssl
import sys
import requests

from bs4 import BeautifulSoup 
app = Flask(__name__)    

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        return redirect(request.url.replace('http://', 'https://'), code=301)

@app.route('/main', methods = ['POST','GET'])
def login(notices=None):
    try:
        if request.method == 'POST':
            user =request.form['User Name']
            password=request.form['password']
            def dblogin(userid):
                conn = pymysql.connect(host='pknuce.ml', user='root', password ='rlflsdPrh12', db='students', charset='utf8')#준규봇
                curs = conn.cursor()
                curs.execut("SELECT num from students where num=%s;",(userid))
                result = curs.fetchchall()
                tup = ((user,),)
                print(userid)
                if result != tup:
                    return render_template('error.html')
                conn.close()
            
            dblogin(int(user))

            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            # 혹은 options.add_argument("--disable-gpu")
            driver = webdriver.Chrome('/home/ubuntu/chromedriver', options=options)
            driver.get('https://lms.pknu.ac.kr/ilos/m/main/login_form.acl')
            driver.find_element_by_id('usr_id').send_keys(user)
            driver.find_element_by_id('usr_pwd').send_keys(password)
            driver.find_element_by_class_name('site-background-color').click()
            driver.get('https://lms.pknu.ac.kr/ilos/main/main_form.acl')
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            notices = soup.select('#user')
            driver.quit()
            return render_template('ce.html', notices=notices[0].text)
            #return "안녕하세요"
    except:
        user = request.args.get('User Name')
        password=request.args.get('password')
        return render_template('error.html')


if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile="./pem/cert.pem", keyfile="./pem/privkey.pem")
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=ssl_context)
    #ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #ctx.load_cert_chain('/etc/letsencrypt/live/pknuce.ml/cert.pem', '/etc/letsencrypt/live/pknuce.ml/public.pem')




	
