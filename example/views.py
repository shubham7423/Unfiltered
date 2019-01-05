from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .forms import CustomUserCreationForm
from django.contrib.auth import logout,authenticate,login,update_session_auth_hash

from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Post,Comment

from django.contrib import messages
from .forms import PostForm

def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'example/welcome.html', {'posts' : Post.objects.all().order_by('-created_at'), 'cuser':request.user})
            else:
                return render(request, 'example/index.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'example/index.html', {'error_message': 'Invalid login'})
    return render(request, 'example/index.html')


    #return render(request, 'example/index.html', {'foo':'foo12'})
def log_out(request):
    #if request.method == 'POST':
        logout(request)
        #return HttpResponseRedirect(reverse('index'))
        return render(request, 'example/index.html', {'form':'form'} )

def welcome(request):
    if not request.user.is_authenticated:
        return render(request, 'example/index.html')
    else:
        return render(request, 'example/welcome.html', {'posts' : Post.objects.all().order_by('-created_at'), 'cuser':request.user})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/example')

    else:
        form = UserCreationForm()
        args = {'form': form}

        return render(request, 'example/reg_form.html', args)


    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('/example')

    else:
        f = CustomUserCreationForm()
    return render(request, 'example/reg_form.html', {'form': f})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'example/index.html', {'error_message': ''})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'example/change_password.html', {'form': form})



def create_post(request):
    if not request.user.is_authenticated:
        return render(request, 'example/index.html')
    else:
        if request.method == 'POST':

            post = Post(catagory = request.POST['catagory'] , user = request.user , post_title = request.POST['title'] , content = request.POST['content'] )

            post.save()
            #messages.success(request,'Your post was created successfully')
            return render(request, 'example/welcome.html', {'posts' : Post.objects.all().order_by('-created_at') , 'cuser':request.user})


        return render(request, 'example/add_post.html')


def detail(request,post_id):
    if not request.user.is_authenticated:
        return render(request, 'example/index.html')
    else:
        user = request.user
        post = get_object_or_404(Post, pk=post_id)
        return render(request, 'example/detail.html', {'post': post, 'user': user , 'comment': Comment.objects.all().order_by('-timestamp')})

def add_comment(request,post_id):
    if not request.user.is_authenticated:
        return render(request, 'example/index.html')
    else:
        if request.method == 'POST':
            comment = Comment( post = get_object_or_404(Post, pk=post_id) , user = request.user, content = request.POST['content'] )

            comment.save()
            #messages.success(request, 'Your comment was added.')
            #return render(request, 'example/welcome.html', {'posts' : Post.objects.all().order_by('-created_at') , 'cuser':request.user})
            return render(request, 'example/detail.html', {'post': get_object_or_404(Post, pk=post_id), 'user': request.user , 'comment': Comment.objects.all().order_by('-timestamp')})


        user = request.user
        post = get_object_or_404(Post, pk=post_id)
        return render(request, 'example/detail.html', {'post': post, 'user': user , 'comment': Comment.objects.all().order_by('-timestamp')})


def delete_post(request,post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    post = Post.objects.filter(user=request.user)
    return render(request, 'example/welcome.html', {'posts' : Post.objects.all().order_by('-created_at') , 'cuser':request.user})

def edit_post(request,post_id):
    if not request.user.is_authenticated:
        return render(request, 'example/index.html')
    else:
        if request.method == 'POST':
            post = Post.objects.get(pk=post_id)
            post.catagory = request.POST['catagory']
            post.post_title = request.POST['title']
            post.content = request.POST['content']
            post.save(['catagory'],['post_title'],['content'])
            #messages.success(request,'Your post was updated successfully')
            return render(request, 'example/welcome.html', {'posts' : Post.objects.all().order_by('-created_at') , 'cuser':request.user})


        return render(request, 'example/update_post.html' , {'posts': get_object_or_404(Post, pk=post_id)} )

def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'example/index.html')
    else:
        return render(request, 'example/dashboard.html', {'posts' : Post.objects.filter(user=request.user).order_by('-created_at'), 'cuser':request.user})

def detailed_cat(request,cat):
    if not request.user.is_authenticated:
        return render(request, 'example/index.html')
    else:
        return render(request, 'example/detailed.html', {'cat' : cat , 'posts' : Post.objects.filter(catagory=cat).order_by('-created_at'), 'cuser':request.user})

def delete_comment(request,comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    comment = Comment.objects.filter(user=request.user)
    return render(request, 'example/welcome.html', {'posts' : Post.objects.all().order_by('-created_at') , 'cuser':request.user})
    #return render(request, 'example/detail.html', {'post': xyz, 'user': request.user , 'comment': Comment.objects.all().order_by('-timestamp')})
