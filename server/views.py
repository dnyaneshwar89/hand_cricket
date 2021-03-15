import socket,random,sys
from _thread import *

from django.shortcuts import render
from .models import LeaderBoard
# Create your views here.

def server_socket():
    HOST = 'localhost'
    PORT = 9994
    try :
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as msg:
        print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    try:
	    server.bind((HOST, PORT))
    except socket.error as msg:
        #print('Bind failed. Error Code : ' + str(msg))
        sys.exit()
        return
    while 1:
	# receive data from client (data, addr)
        d = server.recvfrom(1024)
        data = d[0]
        addr = d[1]
        
        if not data: 
            break
        
        server.sendto(str(random.randint(1,6)).encode('utf-8') , addr)

def index(request):
    start_new_thread(server_socket,())
    top_scores = LeaderBoard.objects.order_by('-score')[:5]
    context = {
        'top_scores':top_scores,
    }
    return render(request,'server.html',context)



