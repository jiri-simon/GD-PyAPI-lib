# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 19:30:55 2014

@author: jirka
"""
from core import  RequestURL2
import sys

def createUser(hostname,GDCAuthTT,domain,username,email,passwd,firstName,lastName,ssoProvider):

    if ssoProvider != "":
         values = """
  {
    "accountSetting": {
      "login": "%s",
      "password": "%s",
      "email": "%s",
      "verifyPassword": "%s",
      "firstName": "%s",
      "lastName": "%s",
      "ssoProvider": "%s"
    }
  }
""" % (username,passwd,email,passwd,firstName,lastName,ssoProvider)
    else:
        values = """
  {
    "accountSetting": {
      "login": "%s",
      "password": "%s",
      "email": "%s",
      "verifyPassword": "%s",
      "firstName": "%s",
      "lastName": "%s"
    }
  }
""" % (username,passwd,email,passwd,firstName,lastName)

    
    headers = { 'Accept': 'application/json','Content-Type': 'application/json'}
    headers["Cookie"] =  "$Version=0; GDCAuthTT=%s;"% GDCAuthTT
    
    url = "%s/gdc/account/domains/%s/users" % (hostname, domain) 
    
    CallGetUser=RequestURL2(url,values,headers,'POST')
    return CallGetUser


def deleteUser(hostname,GDCAuthTT,userid):
    
    headers = { 'Accept': 'application/json','Content-Type': 'application/json'}
    headers["Cookie"] =  "$Version=0; GDCAuthTT=%s;"% GDCAuthTT
    url= hostname+userid
    CallDeleteUser=RequestURL2(url,"",headers,'DELETE')
    return CallDeleteUser

def getUsers(hostname,GDCAuthTT,domain):
    headers = {"Accept": "application/json"}
    headers["Cookie"] =  "$Version=0; GDCAuthTT="+GDCAuthTT+"; $Path=/gdc/account"
    url = "%s/gdc/account/domains/%s/users"% (hostname, domain)
    CallGetUsers=RequestURL2(url,"",headers,'GET')
    return CallGetUsers
    
def ChangePasswdUser(hostname,GDCAuthTT,userid,FirstName,LastName,adminid,passw):

    if userid.split('/', 4 )[4] == adminid.split('/', 4 )[4] :
        print "This user is admin, dont change password, skipped" 
        sys.exit
    else :
       # print "change password of user %s" % (userid)
        values = """
  {
    "accountSetting": {
      "password": "%s",
      "verifyPassword": "%s",
      "firstName":"%s",
      "lastName":"%s"
    }
  }
""" %(passw,passw,FirstName,LastName)
        headers = { 'Accept': 'application/json','Content-Type': 'application/json'}
        headers["Cookie"] =  "$Version=0; GDCAuthTT="+GDCAuthTT+"; $Path=/gdc/account"
        url = hostname + userid
        CallChangePasswd=RequestURL2(url,values,headers,'PUT')
        return CallChangePasswd
         #print "Password for user %s %s has been successfully changed" % (FirstName, LastName)
