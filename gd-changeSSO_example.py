# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 11:39:27 2014

@author: jirka
"""


import sys
sys.path.insert(0, './GDlib')
from core import getTT, logIn
from user import getUsers,ChangeUserSSO, gedUserDetail

import json
import settings


###############################################################################################

###############################################################################################


##Login
LogIn = logIn(settings.GDHostname,settings.GDAdmin_username , settings.GDAdmin_password)

GDCAuthSST = LogIn['GDCAuthSST']  #Get SST
adminid = LogIn['Profile']        #Get Profile of loged user
GDCAuthTT= getTT(settings.GDHostname,GDCAuthSST)      #set Variable GDCAuthTT
GetDomainUsers=getUsers(settings.GDHostname,GDCAuthTT,settings.GDDomain) 
json_acceptable_string = GetDomainUsers['read'].replace("'", "\"")
d = json.loads(json_acceptable_string)
iterace = d['accountSettings']['items']

for item in iterace:
       res=ChangeUserSSO(settings.GDHostname,GDCAuthTT,item['accountSetting']['links']['self'],"gooddata.jiri.simon",item['accountSetting']['firstName'],item['accountSetting']['lastName'])
       print res['code']
       print res['read']
       userDetail = gedUserDetail(settings.GDHostname,GDCAuthTT,adminid.split('/', 4 )[4])
       print json.loads(userDetail['read'])['accountSetting']['links']['self']
       print json.loads(userDetail['read'])['accountSetting']['firstName']
       print json.loads(userDetail['read'])['accountSetting']['lastName']
       print json.loads(userDetail['read'])['accountSetting']['ssoProvider']
