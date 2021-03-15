from django.shortcuts import render
import random,socket
from _thread import *
from server.models import LeaderBoard
# Create your views here.
def client_socket():
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    except socket.error:
	    print('Failed to create socket')
	    sys.exit()
    host = 'localhost'
    port = 9994
    try:
        client.sendto("Send a number".encode('utf-8'),(host,port))
        d = client.recvfrom(1024)
        global server_score
        server_score = d[0].decode('utf-8')
    except socket.error as msg:
            print('Error code client : ' + str(msg))
def index(request):
    context={
        'score':"",
        'server_score':"",
        'final_score':0,
        'wickets':0,
    }
    username = request.GET.get('username')
    game_end=False
    if request.method == 'GET':
        user = LeaderBoard(name=username,score=0)
        user.save()
    if request.method == 'POST':
        start_new_thread(client_socket,())
        score = request.POST.get('score','')
        try:
            server_score
        except:
            server_score = random.randint(1,6)
        final_score = request.session.get('final_score'+username,0)
        if final_score == 0 and server_score != int(score):
            request.session['final_score'+username] = int(score)
            final_score = request.session['final_score'+username] 
        elif server_score != int(score):
            print("going in")
            request.session['final_score'+username] = int(request.session['final_score'+username]) + int(score)
            final_score = request.session['final_score'+username]
        #server_score: random.randint(1,6)
        msg = "Nice..Keep Going"
        if score == '6':
            msg = "Whoaaaa!!! Sixxxx..."
        if score == '4':
            msg = "Whoaaaa!!! Fourr..."
        if server_score == int(score):
            request.session['wickets'+username] = request.session['wickets'+username] + 1
            msg = "Outtt!!"
            wickets = request.session['wickets'+username]
        if request.session['wickets'+username] == 3:
            curr_user = LeaderBoard.objects.get(name=request.GET.get('username'))
            curr_user.score = final_score
            curr_user.save()
            game_end=True
        context = {
            'score':score,
            'server_score': server_score,
            'msg':msg,
            'final_score':final_score,
            'wickets':request.session.get('wickets'+username,'0'),
            'username':username,
            'game_end':game_end,
        }
    else:
        request.session['final_score'+username] = 0
        request.session['wickets'+username] = 0
    return render(request,'client.html',context)