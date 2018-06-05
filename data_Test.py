import re
import win32com.client #pip install pypiwin32 to work with windows operating sysytm
import datetime
import os
import json
import ast
import psycopg2 as p
import psycopg2.extras as e
import time

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
            #message.delete()
            return body_content
            break


def dataFormate(rowdata):
    fs = open('data.txt', 'w+')
    
    fs.write(rowdata)
    fs.close()
    fs = open('data.txt', 'r')
    l= []

    fss = open('dataFromOneServer.txt', 'w+')
    copy = False
    for line in fs:
        if line.strip() == "Start":
            copy = True
        elif line.strip() == "End":
            copy = False
            l= []

        elif copy:
            searchfor= line.split('!')
            if len(l)==0:
                l.append(searchfor[0])
            else:
                l[0]=l[0]+searchfor[0].lstrip()                           
                fss.write(l[0])
        
    fss.close()       

    fsss = open('dataFromOneServer.txt', 'r')

    dbinsertdata=[]
    for mmm in fsss:
           
        datadict=ast.literal_eval(mmm)#toconvert str into dict
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
        #printnt OldIndex
        NewIndex = OldIndex+1
        indexFile1.write(str(NewIndex))
        indexFile1.close()
        #print 'New',NewIndex
        dbinsertdata.append('{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}'.format(NewIndex,datalist[0],datalist[1],datalist[2],datalist[3],datalist[4],datalist[5],datalist[6],json.dumps(datalist[7]),json.dumps(datalist[8])))
        #printnt dbinsertdata
    
    
    print 'Formating Done!!!!'
    return dbinsertdata



def dbfiller(*dbinsertdata):    
    fo = open('kpidataout.txt', 'w+')
    for kkk in dbinsertdata:
        fo.write(kkk)
        fo.write('\n')
    fo.close()
    ServerList={
		'ipi-pilot-prep1':'ipi_pilot_prep1',
		'ipi-pilot-prep2':'ipi_pilot_prep2',
		'ipi-pilot-prep3':'ipi_pilot_prep3',
        }

    foo = open('kpidataout.txt', 'r')
    for kkkk in foo:
        lo=kkkk.split("|")
        print ServerList[lo[1]]
        
        con = p.connect("dbname='GeoprobeDb' user='postgres' password='DESHec1/'")
        cur = con.cursor()
        ha = open('TempValueStorage.txt', 'w')
        ha.write(kkkk)
        ha.close
        
        fhandle = open('TempValueStorage.txt', 'r')
        #fhandle = open('kpidataout.txt','r')
        cur.copy_from(fhandle,'"MonitoringApp_{0}"'.format(ServerList[lo[1]]),sep="|")
        con.commit()
        time.sleep(2)
        
    foo.close()
    #print 'Filled in DB'
   
    
rowdata = save_attachments("51634494",1)
#print rowdata
dbinsertdata = dataFormate(rowdata)
#print dbinsertdata
dbfiller(*dbinsertdata)
