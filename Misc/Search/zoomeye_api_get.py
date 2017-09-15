#!/usr/bin/env python
#! -*- coding: utf8 -*-

import requests
import json
import os
import getopt
import sys

access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6ImplZmZ6aGFuZ0B5b3BtYWlsLmNvbSIsImlhdCI6MTUwMjY3ODA3MywibmJmIjoxNTAyNjc4MDczLCJleHAiOjE1MDI3MjEyNzN9.3F4_cIkFi7tjG8K3tceIi2yoOfqB1h9hTzV_u_Vjuhs'
#access_token 获取方式：curl -X POST https://api.zoomeye.org/user/login -d '{"username":"you_mail","password":"you_passwd"}'
page = 1       #默认获取1页结果

def getHostResponse():
    headers = {'Authorization' : 'JWT ' + access_token}
    urls = 'https://api.zoomeye.org/host/search' + query + "&page=" + str(page)
    respond = requests.get(url = urls, headers = headers)
    if respond.status_code == 401:
        print 'Invalid Token'
    return respond

def getWebResponse():
    headers = {'Authorization' : 'JWT ' + access_token}
    urls = 'https://api.zoomeye.org/web/search' + query
    respond = requests.get(url = urls, headers = headers)
    if respond.status_code == 401:
        print 'Invalid Token'
    return respond

def getHostResult():
    result = json.loads(getHostResponse().text)
    output = open('ip_result.txt','a+') 
    for x in result['matches']:
        print (str(x['ip']) + ':' + str(x['portinfo']['port']))
        output.write(str(x['ip']) + ':' + str(x['portinfo']['port']) + '\n')
    output.close()

def getWebResult():
    result = json.loads(getWebResponse().text)
    output = open('ip_result.txt','a+') 
    for x in result['matches']:
        print x['site']
        output.write(str(x['site']) + '\n')
    output.close()

def usage():
    print '''Usage: python zoomeye.py -s zabbix -w -p 80
    TARGET SPECIFICATION:
    -s: Search app,os name
    -w: Search web
    -o: Search host
    -h: Help
    '''

def main():
    global query
    try:
        opts,args = getopt.getopt(sys.argv[1:], "wohs:", ['web', 'os', 'search', 'port'])
        for opt,args in opts:
            if opt in ("-h", "--help"):
                usage()
            elif opt in ("-s", "--search"):
                #query = '?query=' + args + '&' + 'page=' + str(page) + '&' + 'facet=app,os'
                query = '?query=' + args + '&' + 'facet=app,os'
            elif opt in ('-w', "--web"):
                getWebResult()
            elif opt in ('-o', "--os"):
                getHostResult()
    except getopt.GetoptError:
        usage()

if __name__ == '__main__':
    main()