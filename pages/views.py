from django.shortcuts import render,redirect ,get_object_or_404 # for showing and moving trough html pages
from django.http import JsonResponse # for sending json data withn html
from django.contrib.auth import authenticate, login # for authentication (login and logout)
from .models import LogInUsers , UserBlogs ,Like
from .forms import LogInForm , BlogsForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def EditBlog(request,blog_id):
    blog = UserBlogs.objects.get(id=blog_id)
    
    if request.method == 'POST':
        blog.description=request.POST.get('description')
        blog.save()
        return redirect('MyBlogs',user_email=request.session.get('email'))
    return render(request, 'pages/EditBlog.html',{'blog':blog,'form':BlogsForm})

def MyBlogs(request,user_email):
    user_id = LogInUsers.objects.get(email=user_email)
    blogs = UserBlogs.objects.filter(user=user_id)
    return render(request, 'pages/MyBlogs.html',{'blogs':blogs,'currentUser':request.session.get('email')})

def Blogs(request):
    return render(request, 'pages/Blogs.html',{'blogs':UserBlogs.objects.all() ,'currentUser':request.session.get('email')})

def LogIn(request):    
    try :
        if request.method == 'POST':
            form = LogInForm(request.POST) # form instance with email and password data
            if form.is_valid(): # form validation
                print("form is valid")
                entered_email =request.POST['email'] # get entered email
                entered_password =request.POST['password'] # get entered password
                exist_email =LogInUsers.objects.filter(email=entered_email).count() # check if email exist
                if exist_email == 1: # account already exist then check on password
                    exist_password =LogInUsers.objects.get(email=entered_email) # get password
                    if exist_password.password== entered_password: # valid password
                        #checks whether the provided credentials (username and password) are valid.
                        user = authenticate(request, username=entered_email, password=entered_password)
                        login(request, user) #This creates a session for the user, allowing them to stay logged in across requests.
                        request.session['email'] = entered_email # store email in email session
                        return redirect('Blogs') #move to tasks page
                    else : # the email is correct but password is wrong
                        return render(request, 'pages/LogIn.html',{"form":LogInForm,'error':2})
                else: # invaild email
                    return render(request, 'pages/LogIn.html',{"form":LogInForm,'error':1})
    except Exception as exception:
        print(exception)
    return render(request, 'pages/LogIn.html',{"form":LogInForm})

def Register(request):    
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            entered_email =request.POST['email']
            exist_email =LogInUsers.objects.filter(email=entered_email).count()
            if exist_email == 1: # account already exist
                return render(request, 'pages/Register.html',{"form":LogInForm,'error':1})
            else:   # new account add it to db
                form.save()
                return redirect('LogIn')
    return render(request, 'pages/Register.html',{"form":LogInForm})

# View to create a new blog post (Only for logged-in users)
@login_required(login_url='LogIn')
def CreateBlog(request):
    # Get the current user based on session email
    user_email = request.session.get('email')
    if not user_email:
        return redirect('LogIn')  # If no user is logged in, redirect to login page
    
    if request.method == 'POST':
        form = BlogsForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = LogInUsers.objects.get(email=user_email)  # Assign the logged-in user
            blog.save()
            return redirect('Blogs')  # Redirect to the blog list page
    else:
        form = BlogsForm()
    
    return render(request, 'pages/CreateBlog.html',{"form":form,'currentUser':request.session.get('email')})

@login_required(login_url='LogIn')
def LikeBlog(request,blog_id):
    blog = UserBlogs.objects.get(id=blog_id) 
    current_user = request.session.get('email')
    user_id = LogInUsers.objects.get(email=current_user).id
    # Check if the user has already liked the blog
    if not Like.objects.filter(user=user_id,blog=blog).exists():
        user = LogInUsers.objects.get(id=user_id)
        Like.objects.create(user=user,blog=blog)
        
    return redirect('BlogDetail',slug=blog.slug)

@login_required(login_url='LogIn')
def UnLikeBlog(request,blog_id):
    blog = UserBlogs.objects.get(id=blog_id) 
    current_user = request.session.get('email')
    user_id = LogInUsers.objects.get(email=current_user).id
    # Check if the user has already liked the blog
    like = Like.objects.filter(user=user_id,blog=blog).first() # return the first object from a QuerySet, or None if no object matches the query.
    if like:
        like.delete()
    return redirect('BlogDetail',slug=blog.slug)

def BlogDetail(request,slug):
    current_user = request.session.get('email')
    user_id = LogInUsers.objects.get(email=current_user).id
    
    blog = UserBlogs.objects.get(slug=slug)
    flag = blog.like_set.filter(user=user_id).exists()
    return render(request, 'pages/BlogDetail.html',{'blog':blog,'currentUser':current_user,'flag':flag})

def Authorlogs(request,blog_id):
    user_email = UserBlogs.objects.get(id=blog_id).user
    blogs =UserBlogs.objects.filter(user=user_email)
    return render(request, 'pages/AuthorBlogs.html',{'blogs':blogs,'currentUser':request.session.get('email')})