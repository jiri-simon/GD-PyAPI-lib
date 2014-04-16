# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 19:31:31 2014

@author: jirka
"""
from core import  RequestURL2
from json import dumps

def createNewProject(hostname,GDCAuthTT,token,title,summary):
    headers = { 'Accept': 'application/json','Content-Type': 'application/json'}
    headers["Cookie"] =  "$Version=0; GDCAuthTT=%s;"% GDCAuthTT
    
    values = dumps({ "project" : {
       "content" : { "guidedNavigation": 1, "driver" : "Pg", "authorizationToken" : ""+token+""},
       "meta" : {
       "title" : ""+title+"",
       "summary" : ""+summary+""
       } }
})
    url="%s/gdc/projects"% hostname
    CreateProject=RequestURL2(url,values,headers,'POST')
    return CreateProject


def deleteProject(hostname,GDCAuthTT,projectID):
    headers = { 'Accept': 'application/json','Content-Type': 'application/json'}
    headers["Cookie"] =  "$Version=0; GDCAuthTT=%s;"% GDCAuthTT
    url="%s/gdc/projects/%s"% (hostname, projectID)
    deleteProject=RequestURL2(url,"",headers,'DELETE')
    return deleteProject