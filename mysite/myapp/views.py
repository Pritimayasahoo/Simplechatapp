from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from . models import Room,Account,CustomUser,Message
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.hashers import check_password

@login_required(login_url='login/')
def home(request):
    if request.method=="POST":
        room=request.POST['room']
        password=request.POST['password']
        mail=request.session.get('email')
        user=Account.objects.filter(email=mail).first()
        if user:
            user_name=user.name
            my_room=Room.objects.filter(roomname=room).first()
            if my_room:
                if my_room.roompassword==password:
                    return redirect(f'room/?room={room}&name={user_name}')
                else:
                    messages.info(request,'Please Give correct password')
                    return redirect('/') 

            else:
               Room.objects.create(roomname=room,roompassword=password)
               return redirect(f'room/?room={room}&name={user_name}')    
    return render(request,'home.html')
            

 #print(room)
# my_room=Room.objects.filter(romname=room).first()
# if my_room:
#     return redirect(f'room/?room={room}&name={username}')
# else:
#     Room.objects.create(romname=room)
#     return redirect(f'room/?room={room}&name={username}')
    #return render(request,'home.html')
def Loginuser(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=CustomUser.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            print(user)
            my_user=auth.authenticate(email=email,password=password)
            auth.login(request,my_user)
            request.session['email'] = email
            return redirect('/')
        else:
            messages.info(request,'SOME THING WENT WRONG')
            return redirect('login') 
    return render(request,'login.html')

def createaccount(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        name=request.POST['name']
        user=CustomUser.objects.filter(email=email).first()
        if user:
            messages.info(request,'THIS USER IS ALREADY EXIST')
            return redirect('/createaccount/') 
        CustomUser.objects.create_user(email=email,password=password)
        Account.objects.create(email=email,name=name)
        #user=CustomUser.objects.filter(email=email).first()
        my_user=auth.authenticate(email=email,password=password)
        auth.login(request,my_user)
        request.session['email'] = email
        return redirect('/')

    return render(request,'createaccount.html')    


@login_required(login_url='login/')  
def room(request):
    name=request.GET.get('name')
    room=request.GET.get('room')
    print(name)
    print(room)
    my_room=Room.objects.filter(roomname=room).first()
    allmessages=Message.objects.filter(roomname=my_room.roomname)
    context={
        'room':my_room,
        'messages':allmessages,
        'user':name
    }
    return render(request,'room.html',context)

@login_required(login_url='login/')
def createmessage(request):
    messagevalue=request.GET.get('message')
    room=request.GET.get('room')
    name=request.GET.get('name')
    print(room)
    print(name)
    #username=request.GET.get('username')
    roomname='chiku'
    newmessage=Message.objects.create(message=messagevalue,roomname=room,user=name)
    mtext={
        'text':'message saved'
    }
    return JsonResponse(mtext)

@login_required(login_url='login/')
def Refresh_message(request):
    room=request.GET.get('roomname')
    print(room)
    allmessages=Message.objects.filter(roomname=room)
    num_messages=allmessages.count()
    print(allmessages)
    stext={
        'messages':list(allmessages.values()),
        'num_messages':num_messages
    }
    print(stext)
    return JsonResponse(stext)


