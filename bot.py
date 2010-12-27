import sys 
import socket 
import string 
import os

import time

#HOST='irc.unixfreunde.de'
HOST='irc.freenode.net'
PORT=6667
NICK='system_pybot'
CHANNEL='#wemakeporn'

def parse(data):
    print data
    
    try:
        data=data.rstrip()
        dlist=data.split()
        
        #server ping
        if(dlist[0]=='PING'):
            #pong back to server
            sendcmd('PONG %s' % dlist[1].split(':')[1])
        
        else:
            user=dlist[0].lstrip(':').split('!')[0]
            
            #private message
            if(dlist[1]=='PRIVMSG'):
                if((dlist[2]==NICK) & (checkuser(user))):
                    msg = data.split(':')[2]
                    cmd = msg.split()[0]
                    params = msg.lstrip('%s ' % cmd)
                    
                    if(cmd == 'read'):
                        pastefile(params.split()[0])
                    
                    elif(cmd == 'say'):
                        sendcmsg(params)
                    
                    elif(cmd == 'do'):
                        sendcmd(params)
                    
                    else:
                        errormsg(user, 404)
                    
                else:
                    errormsg(user, 403)
            
            #events: join
            elif(dlist[1]=='JOIN'):
                if((dlist[2].lstrip(':')==CHANNEL) & (checkuser(user))):
                    chanmode('+o', user)
                
    except Exception as e:
        print e
        if (user):
            errormsg(user, 500)

def sendcmsg(msg):
    sendmsg(CHANNEL, msg)
    
def sendmsg(target, msg):
    sendcmd('PRIVMSG %s :%s' % (target, msg))
    time.sleep(1)


def errormsg(target, code):
    msg = '#%s: ' % code
    
    if(code == 403):
        msg += 'permission denied'
    
    elif(code == 404):
        msg += 'not found'
    
    elif(code == 500):
        msg += 'internal bot error'
    
    sendmsg(target, msg)


def pastefile(filename):
    sendcmsg('- START %s -' % filename)
    
    f=open(filename)
    for l in f:
        sendcmsg(l)
    f.close()
    
    sendcmsg('- END -')


def checkuser(user):
    f=open('operators.conf')
    for l in f:
        if (user == l):
            return True
    f.close()
    
    return False


def chanmode(mode, target):
    sendcmd('MODE %s %s %s' % (CHANNEL, mode, target))
    
def sendcmd(cmd):
    s.send('%s\r\n' % cmd)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
sendcmd('NICK %s' % NICK)
sendcmd('USER %s %s %s :%s %s' % (NICK, NICK, NICK, NICK, 'IRC'))
sendcmd('JOIN %s' % CHANNEL)

sendcmsg('> HELLO <')

while 1:
    data=s.recv(4096)
    parse(data)