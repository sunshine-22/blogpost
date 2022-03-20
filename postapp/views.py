from django.shortcuts import render,redirect
from . models import Registration,Post
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from . tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_str
from django.urls import reverse
from django.http import HttpResponse
def dashboard(request,name):
    userdata=Registration.objects.get(email=name)
    image=userdata.profile
    usermail=userdata.email
    username=userdata.username
    displaypost=reversed(Post.objects.all().values())
    
    if(request.method=="POST") and "post" in request.POST:
        img=request.FILES.get("userpost")
        recname=request.POST.get("name")
        recemail=request.POST.get("email")
        desc=request.POST.get("desc")
        datapost=Post(owner=recname,owneremail=recemail,description=desc,images=img)
        datapost.save()
    if(request.method=="POST") and "comments" in request.POST:
        ctrnmae=request.POST.get("crtname")
        crtcmt=request.POST.get("crtcmnt")
        cmtid=request.POST.get("crtid")
        commentdata=ctrnmae+" : "+crtcmt
        newcmt=Post.objects.get(id=cmtid)
        savecmt=newcmt.comments
        newcmt.comments= savecmt+commentdata
        newcmt.save()
    return render(request,"postapp/dashboard.html",{"profile":str(image),"useremail":usermail,"username":username,"postdata":displaypost})
def home(request):
    uname=request.session.get("uname","")
    paswd=request.session.get("paswd","")
    if(request.method=="POST"):
        try:
            username=request.POST.get("email")
            pswd=request.POST.get("password")
            checker=Registration.objects.get(email=username)
            if(checker.is_active==True):
                if(checker.password==pswd):
                    request.session["uname"]=username
                    request.session["paswd"]=pswd
                    return redirect("dashboard/"+str(username))
                else:
                    msg="password not valid"
                    return render(request,"postapp/signin.html",{"msg":msg})
            else:
                    msg="Account not activated"
                    return render(request,"postapp/signin.html",{"msg":msg})
        except:
            msg="User Not Found"
            return render(request,"postapp/signin.html",{"msg":msg})
    return render(request,"postapp/signin.html",{"uname":uname,"paswd":paswd})
def register(request):
    if(request.method=="POST"):
        name=request.POST.get("username")
        useremail=request.POST.get("useremail")
        userdob=request.POST.get("userdob")
        useraddress=request.POST.get("useraddress")
        userprofile=request.FILES.get("userprofile")
        userpassword=request.POST.get("password")
        try:
            user=Registration.objects.create(username=name,email=useremail,dob=userdob,address=useraddress,profile=userprofile,password=userpassword,is_active=False)
        except:
            return render(request,"postapp/register.html",{"message":"User Alredy Exist's"})
        uidb64=urlsafe_base64_encode(force_bytes(user.pk))
        currentsite=get_current_site(request).domain
        link=reverse("activate",kwargs={"uidb64":uidb64,"token":account_activation_token.make_token(user)})
        activate_url="http://"+currentsite+link
        message="hi "+name+" click below link to verify\n"+activate_url
        email=EmailMessage("Account Activation",message,to=[useremail])
        try:
            email.send()
        except:
            return render(request,"postapp/register.html",{"message":"Unable to send E-mail"})
        return render(request,"postapp/register.html",{"message":" verification link send to E-mail"})
    return render(request,"postapp/register.html")
def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=Registration.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,user.DoesNotExist):
        user=None
    if(user is not None and account_activation_token.check_token(user,token)):
       user.is_active=True
       user.save()
       return render(request,"postapp/success.html")
    else:
        return render(request,"postapp/failed.html")
