from django.shortcuts import render, redirect
from .forms import PostForm, ImageForm
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.
def list(request):
    posts = Post.objects.all()
    return render(request, 'posts/list.html',{'posts':posts})

@login_required
def create(request):
    # 1. get방식으로 데이터를 입력할 form을 요청한다.
    # 4. 사용자가 데이터를 입력해서 post방식으로 요청한다.
    # 9. 사용자가 다시 적절한 데이터를 입력해서 post방식으로 요청한다.
    if request.method == "POST": # 저장
        # 5. 10. post방식으로 저장요청을 받고, 데이터를 받아 PostForm에 넣어서 인스턴스화 한다.
        post_form = PostForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        # 6. 11. 데이터 검증을 한다.
        if post_form.is_valid():
            # 12. 적절한 데이터가 들어오는 경우, 데이터를 저장하고 list페이지로 리다이렉트!
            post = post_form.save(commit=False) # 저장이 된 게시물
            post.user = request.user
            post.save()
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(request.POST, request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False) # 잠깐만 기다려~~ 
                    image.post = post
                    image.save()
                    
            return redirect("posts:list")
        # else:
        #     # 7. 적절하지 않은 데이터가 들어오는 경우
        #     pass
    else: # get방식이면 폼을 보여줌
        # 2. PostForm을 인스턴스화 시켜서 form에 저장한다.
        post_form = PostForm()
        image_form = ImageForm()
    # 3. form을 담아서 create.html을 보내준다.
    # 8. 사용자가 입력한 데이터는 form에 담아진 상태로 다시 form을 담아서 create.html을 보내준다.
    return render(request, 'posts/form.html', {'post_form':post_form,'image_form':image_form})
  
@login_required
def update(request, id):
    # 게시물을 수정하려면 기존의 데이터 필요
    post = Post.objects.get(id=id)
    if post.user == request.user: # 지금 로그인한 사람이 게시물을 작성해따
            
        if request.method == "POST":
            post_form = PostForm(request.POST, instance=post) # create와 update는 instance=post 빼고는 구조가 같음.
            if post_form.is_valid():
                post_form.save()
                return redirect("posts:list")
        else:
            post_form = PostForm(instance=post)
        return render(request, 'posts/form.html',{'post_form':post_form})
    else:
        return redirect("posts:list")

@login_required
def delete(request,id):
    post = Post.objects.get(id=id)
    if post.user == request.user:
        post.delete()
        return redirect("posts:list")
    else:
        return redirect("posts:list")