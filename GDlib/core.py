# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 19:29:37 2014

@author: jirka
"""

from urllib2 import Request, urlopen, HTTPError
import json

def RequestURL(request):
 result= dict()  
 try:
        response = urlopen(request)
        result['code']=response.code
        result['info']=response.info()
        result['read']=response.read()
        return result
       
 except HTTPError, err:
        result['code']=err.code
        result['info']=err.info()
        result['read']=err.read()
        return result
        
def RequestURL2(url,data,headers,method):
 result= dict() 
 try:   
        if data == "":
            request = Request(url,  headers=headers)      
        else:
            request = Request(url,data=data, headers=headers) 
        request.get_method = lambda: method 
        response = urlopen(request)
        result['code']=response.code
        result['info']=response.info()
        result['read']=response.read()
        return result
       
 except HTTPError, err:
        result['code']=err.code
        result['info']=err.info()
        result['read']=err.read()
        result['headers']=err.headers
        return result    

def logIn(hostname,username,password):
    result= dict() 
    values = """
  {
    "postUserLogin": {
      "login": "%s",
      "password": "%s",
      "remember": 1
    }
  }
"""% (username ,password)
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url='%s/gdc/account/login' % hostname
    CallLogin=RequestURL2(url,values,headers,'POST')
    if CallLogin['code'] == 200:
        Profile = (json.loads(CallLogin['read'])['userLogin'])['state']
        cookie =   CallLogin['info'].dict['set-cookie'].split(';')
        GDCAuthSST = [s for s in cookie if "GDCAuthSST" in s][0].split('=')[1]
        result['GDCAuthSST'] = GDCAuthSST
        result['Profile'] = Profile  
        print "profile %s"% Profile
    else:
        print "ERROR:  code:%s \n Message: %s \n \n exiting!!!" %(CallLogin['code'],CallLogin['read'])
        exit()
    return result

    
def getTT(hostname,SST):   
    headers = {"Cookie": "", 
        "Accept": "application/json", 
        "Content-Type": "application/json"} 
    headers["Cookie"] = "$Version=0; GDCAuthSST=%s; $Path=/gdc/account"% SST
    url="%s/gdc/account/token"% hostname
    CallAuth=RequestURL2(url,"",headers,'GET')
    if CallAuth['code'] == 200:
       GDCAuthTT =CallAuth['info'].dict['set-cookie'].split(';')[0].split('=')[1]  
    else:
        print "ERROR:  code:%s \n Message: %s \n \n exiting!!!" %(CallAuth['code'],CallAuth['read'])
        exit()
    return GDCAuthTT    

def logOut(hostname,GDCAuthTT,userid):
    headers = {"Accept": "application/json"}
    headers["Cookie"] =  "$Version=0; GDCAuthTT=%s; $Path=/gdc/account"% GDCAuthTT
    print headers
    print userid
    url = hostname + userid
    print url
    CallLogout=RequestURL2(url,"",headers,'DELETE')
    if CallLogout['code'] == 200:
        print "User logout: %s"%CallLogout['read']
    else:
     #   print "ERROR:  code:%s \n Message: %s \n \n exiting!!!" %(CallLogout['code'],CallLogout['read'])
        exit()
          