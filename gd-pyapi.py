# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 11:39:27 2014

@author: jirka
"""


from urllib2 import Request, urlopen, HTTPError
import sys
sys.path.insert(0, './GDlib')
from core import getTT, logIn,logOut,RequestURL2
from user import getUsers, ChangePasswdUser, createUser, deleteUser
import json
import settings


###############################################################################################

   

def getRoleSummary(hostname,role,GDCAuthTT):
    headers = {"Accept": "application/json"}
    headers["Cookie"] = GDCAuthTT
    url = hostname+role
    request = Request(url, headers=headers)
    response_body = urlopen(request)
    roleSummary =  ((json.loads(response_body.read())['projectRole'])['meta'])['title']
    return roleSummary

def getRoles(projectid,GDCAuthTT):
    rolesDetails={}
    headers = {"Accept": "application/json"}
    headers["Cookie"] = GDCAuthTT
    url = "https://secure.gooddata.com/gdc/projects/"+projectid+"/roles"
    request = Request(url, headers=headers)
    response_body = urlopen(request)#.read()
    roles =  (json.loads(response_body.read())['projectRoles'])['roles']
    for role in roles:
        rolesDetails[role] = getRoleSummary(role,GDCAuthTT)     
    return rolesDetails 



def getUserbyName(domain,username,GDCAuthTT):
    headers = {"Accept": "application/json"}
    headers["Cookie"] = GDCAuthTT
    url = "https://secure.gooddata.com/gdc/account/domains/"+domain+"/users?login="+username
    print url
    request = Request(url, headers=headers)
    response_body = urlopen(request)
    userprofile =  ((((((json.loads(response_body.read()))['accountSettings'])['items'])[0])['accountSetting'])['links'])['self']
    #print ((((((json.loads(response_body.read()))['accountSettings'])['items'])[0])['accountSetting'])['links'])['self']
    return userprofile 


    
    
def addUsertoProject(projectid,roleid,userid, GDCAuthTT):
        values = "{ \"user\" : {\n     \"content\" : {\n           \"status\":\"ENABLED\",\n           \"userRoles\":[\"%s\"]\n                 },\n     \"links\"   : {\n           \"self\":\"%s\"\n                }\n    }\n}"%(roleid,userid)
        print values
        headers = {"Accept": "application/json"}
        headers["Cookie"] = GDCAuthTT
        print headers
        url = "https://secure.gooddata.com/gdc/projects/"+projectid+"/users"
        print url
        try:
            request = Request(url, data=values, headers=headers)
            response_body = urlopen(request).read()
            print response_body    
        except HTTPError, err:
            print err.code
            print err.read()







    

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

user=createUser(settings.GDHostname,GDCAuthTT,settings.GDDomain,"jirkuv1@test.cz","jirkuv1@test.cz","Heslo123","TestJmeno","TestPrijmeni","")
print user['code']
print user['read']

deletedUser=deleteUser(settings.GDHostname,GDCAuthTT,"/gdc/account/profile/589124c2f127f09fe803a22ceb66cf2e")
print deletedUser['code']
print deletedUser['read']


#for item in iterace:
#     ChangePasswdUser(settings.GDHostname,GDCAuthTT,item['accountSetting']['links']['self'],item['accountSetting']['firstName'],item['accountSetting']['lastName'],adminid,"SecretPassword")

#logOut(settings.GDHostname,GDCAuthTT,adminid)
