#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request, render_template
from selenium import webdriver
import ssl
import sys
import requests
import pymysql
from bs4 import BeautifulSoup

app = Flask(__name__)    

@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/main', methods = ['POST','GET'])
def login(notices=None):
    try:
        if request.method == 'POST':   
            user =request.form['User Name']
            password=request.form['password']
            def dblogin(userid):
                conn = pymysql.connect(host='host주소', user='userId', password ='비밀번호', db='db명', charset='utf8')
                curs = conn.cursor()
                curs.execute("SELECT EXISTS (SELECT num from students where num=%s) as success", userid)
                result = curs.fetchall()[0][0]
                conn.close()
                return result
            confirm = dblogin(int(user))
            app.logger.debug(int(user))
            if confirm == 1:
			//셀레니움을 이용해 ID와 PW를 받으면 DB에 저장하지 않고 바로 포털사이트에 대입하는 방법.
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument('window-size=1920x1080')
                options.add_argument("disable-gpu")
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                driver = webdriver.Chrome('/home/ubuntu/webtest/templated/chromedriver', options=options)
                driver.get('https://lms.pknu.ac.kr/ilos/m/main/login_form.acl')
                driver.find_element_by_id('usr_id').send_keys(user)
                driver.find_element_by_id('usr_pwd').send_keys(password)
                driver.find_element_by_class_name('site-background-color').click()
                driver.get('https://lms.pknu.ac.kr/ilos/main/main_form.acl')
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                notices = soup.select('#user')
                driver.quit()
		//대입이 성공하면 ce.html 반환
                return render_template('ce.html', notices=notices[0].text)
            else:
		//실패시 error.html 반환
                return render_template('error.html')
            #return "안녕하세요"

//예외 발생시 error.html 반환
    except:
        user = request.args.get('User Name')
        password=request.args.get('password')
        return render_template('error.html')


if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile="./pem/cert.pem", keyfile="./pem/privkey.pem")
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=ssl_context)
    #ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #ctx.load_cert_chain('/etc/letsencrypt/live/pknuce.ml/cert.pem', '/etc/letsencrypt/live/pknuce.ml/public.pem')




	
