import re
import win32com.client #pip install pypiwin32 to work with windows operating sysytm
import datetime
import os
import json
import ast
import psycopg2 as p
import psycopg2.extras as e

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
folder=outlook.Folders("desh.deepakpandey@team.telstra.com")
inbox = folder.Folders("Inbox")
messages=inbox.Items


def save_attachments(subject,which_item):
    # To iterate through inbox emails using inbox.Items object.
    for message in messages:
        if (message.Subject == subject):
            print "Mail Found"
            body_content = message.body
            #print body_content
            message.delete()
            return body_content
            break


def dataFormate(rowdata):
    fs = open('data.txt', 'w+')
    
    fs.write(rowdata)
    fs.close()
    fs = open('data.txt', 'r')
    l= []
    
    for i in fs:
        searchfor= i.split('!')
        if len(l)==0:
            l.append(searchfor[0])
        else:
            l[0]=l[0]+searchfor[0]
    datadict=ast.literal_eval(l[0])#toconvert str into dict
    datakeys=datadict.keys()
    ############## data formate as per the db ################
    datalist=[]
    datalist.append(datadict['server_name'])
    datalist.append(datadict['current_date_time'])
    datalist.append(datadict['cpu_percent'])
    datalist.append(datadict['total_mem_usage'])
    datalist.append(datadict['total_mem_available'])
    datalist.append(datadict['total_swap_usage'])
    datalist.append(datadict['total_swap_available'])
    datalist.append(datadict['processes'])
    datalist.append({"disk_usage":datadict['disk_usage']})
    ##########################################################
    #print datalist[8]
        
    #print type(datadict), datadict
    #fo.write(json.dumps(l[0]))
    #print datalist[8]
    
    indexFile=open('IndexProvider.txt', 'r')
    OldIndex =int(indexFile.readline())
    indexFile.close()
    indexFile1=open('IndexProvider.txt', 'w')
    #print OldIndex
    NewIndex = OldIndex+1
    indexFile1.write(str(NewIndex))
    indexFile1.close()
    #print 'New',NewIndex
    dbinsertdata = '{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}'.format(NewIndex,datalist[0],datalist[1],datalist[2],datalist[3],datalist[4],datalist[5],datalist[6],json.dumps(datalist[7]),json.dumps(datalist[8]))
    #print dbinsertdata
    
    
    print 'Formating Done!!!!'
    return dbinsertdata


def dbfiller(dbinsertdata):
    fo = open('kpidataout.txt', 'w+')
    fo.write(dbinsertdata)
    fo.close()
    con = p.connect("dbname='GeoprobeDb' user='postgres' password='DESHec1/'")
    cur = con.cursor()
    fhandle = open('kpidataout.txt','r')
    cur.copy_from(fhandle,'"MonitoringApp_spiserver"',sep="|")
    con.commit()
    

    print 'Filled in DB'
   
    
rowdata = save_attachments("kpidata",1)
dbinsertdata = dataFormate(rowdata)

dbfiller(dbinsertdata)
