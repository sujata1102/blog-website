from django.shortcuts import render,HttpResponse,redirect
from blogapp.models import Post
from django.db.models import Q
from blogapp.forms import StudentForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from blogapp.forms import UserForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    
    #return HttpResponse("Hello All, This is first response!!!")
    print("In home function")
    return redirect('/udash')

def contact(request):
    
    return HttpResponse("Hello from contact")

def event(request):
    
    return HttpResponse("Hello from event")

def company(request):
    
    return HttpResponse("Hello from company")

#passing data from views to html file

def view_html(request):
    # data={'name':'Itvedant','location':'Eclass','module':'Django'}
    # data['name']="Itvedant"
    data={}
    data['d']=[100,200,300,400,500]
    # data['x']=100
    # data['x']=400
    # data['y']=200
    return render(request,'udashboard.html',data)

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def index(request):

    q1=Q(is_deleted=1)
    q2=Q(active=1)
    # rec=Post.objects.filter(q1 & q2).order_by('dt') <-- asending
    rec=Post.objects.filter(q1 & q2).order_by('-dt')  #<-- descending
    content={}
    content['data']=rec
    return render(request,'index.html',content)

def post(request):
    return render(request,'post.html')

def create_post(request):
    userid=request.user.id
    print("Logged in user id:",userid)
    if request.method=="POST":
        t=request.POST['ptitle']
        s=request.POST['sdesc']
        d=request.POST['det_desc']
        c=request.POST['cat']
        act=request.POST['pactive']
        '''
        print("Title:",t)
        print("Small Description:",s)
        print("Details:",d)
        print("Category:",c)
        print("Whether Active:",act)
        '''
        p=Post.objects.create(title=t,sdesc=s,det=d,cat=c,active=act,is_deleted="1",uid=userid)
        #print(p)
        p.save()
        #return HttpResponse("Record is inserted successfull")
        return redirect('/udash')
    else:
        return render(request,'create_post.html')
    
def user_dashboard(request):
    #rec=Post.objects.all()
    # print(rec)
    userid=request.user.id
    q1=Q(is_deleted=1)
    q2=Q(uid=userid)
    rec=Post.objects.filter(q1 & q2)
    content={}
    content['data']=rec

    return render(request,'udashboard.html',content)    

def delete(request,rid):
    # p=Post.objects.get(id=rid)
    # p.delete()
    p=Post.objects.filter(id=rid)
    p.update(is_deleted="0")

    return redirect('/udash')

def edit(request,rid):
    
    if request.method=="POST":
        utitle=request.POST['ptitle']
        usdesc=request.POST['sdesc']
        udet=request.POST['det_desc']
        ucat=request.POST['cat']
        uactive=request.POST['pactive']

        p=Post.objects.filter(id=rid)
        p.update(title=utitle,sdesc=usdesc,det=udet,cat=ucat,active=uactive)

        return redirect('/udash')

    else:
        p=Post.objects.get(id=rid)
        # print(p)
        content={}
        content['data']=p
        return render(request,'edit.html',content)

#filters start

def catfilter(request,catopt):
    q1=Q(cat=catopt)
    q2=Q(is_deleted=1)
    rec=Post.objects.filter(q1 & q2)
    content={}
    content['data']=rec

    return render(request,'udashboard.html',content)

def actfilter(request,actopt):
    q1=Q(active=actopt)
    q2=Q(is_deleted=1)
    rec=Post.objects.filter(q1 & q2)
    content={}
    content['data']=rec

    return render(request,'udashboard.html',content)

def djangoform(request):
    fm=StudentForm()
    content={}
    content['form']=fm
    return render(request,'djangoform.html',content)
    
def user_register(request):
    if request.method=="POST":
        # fm=UserCreationForm(request.POST)
        fm=UserForm(request.POST)
        if fm.is_valid():
            fm.save()#inserting username and password in auth_user table
            return HttpResponse("User Created Successfully!!!")
        else:
            return HttpResponse("Failed to create user")
    else:
        # fm=UserCreationForm()
        fm=UserForm()
        content={}
        content['form']=fm
        return render(request,'register.html',content)

def user_login(request):
    if request.method=="POST":
        fm=AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data["username"]
            upass=fm.cleaned_data["password"]

            u=authenticate(username=uname, password=upass)
            if u:
                login(request,u)
                return redirect('/udash')
        else:
            content={}
            content['data']="Invalid Username and Password"
            content['form']=fm
            return render(request,'login.html',content)

    else:
        fm=AuthenticationForm()
        content={}
        content['form']=fm
        return render(request,'login.html',content)

def user_logout(request):
    logout(request) #To destroy session
    return redirect('/')

def setcookies(request):
    res=render(request,'setcookie.html')#store response object
    res.set_cookie('name','ITVEDANT')
    res.set_cookie('per',98.7)
    res.set_cookie('rno',45)
    return res

def getcookies(request):
    content={}
    content['n']=request.COOKIES['name']
    content['p']=request.COOKIES['per']
    content['r']=request.COOKIES['rno']

    return render(request,'getcookie.html',content)

def setsession(request):
    request.session['username']="sujata11"
    request.session['password']="redhat123@"
    return render(request,'setsession.html')

def getsession(request):
    data={}
    data['uname']=request.session['username']
    data['upass']=request.session['password']
    return render(request,'getsession.html',data)