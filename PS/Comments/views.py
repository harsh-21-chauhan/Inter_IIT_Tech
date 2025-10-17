from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
from django.contrib.auth.models import User
from .models import Post, Comment


# Create your views here.
def home(request):
  posts = Post.objects.all()
  if request.user.is_anonymous:
   return redirect("/login")
  return render(request,'index.html',{'posts':posts}) 

def loginUser(request):
  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username=username,password=password)

    if user is not None:
      login(request,user)
      return redirect('/')

    else :
      return render(request,'login.html')
  return render(request, 'login.html')    


def logoutUser(request):
  logout(request)
  return redirect('/login')

def postDetail(request,post_id):
 post = get_object_or_404(Post, id=post_id)

    # Only top-level comments
 comments = post.comments.filter(parent__isnull=True).order_by('created_at')

 if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get("content")        # Comment text
        parent_id = request.POST.get("parent_id")    # Optional: parent comment ID

        parent_comment = None
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)

        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content,
                parent=parent_comment
            )

        # Redirect to avoid resubmission on refresh
        return redirect(request.path)

 return render(request, 'post_details.html', {
        'post': post,
        'comments': comments
    })