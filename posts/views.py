from django.shortcuts import render, redirect
from .forms import PostForm, ImageForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
def list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    return render(request, 'posts/list.html',{'posts':posts,'comment_form':comment_form})

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
    # 지우고싶은 게시물 찾고
    post = Post.objects.get(id=id)
    # 로그인한 유저랑 게시물작성 유저랑 같은지 확인
    if post.user == request.user:
        post.delete()
    return redirect("posts:list")


@login_required
@require_POST # comment_create가 POST방식이 아닐 땐 튕김.
def comment_create(request, post_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = Post.objects.get(id=post_id)
            comment.save() # auto_now_add 를 이미 줘서 그냥 저장됨.
            return redirect("posts:list")
    
@login_required
def comment_delete(request, post_id, comment_id):
    # 코멘트 찾기
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
    return redirect("posts:list")

# 이건 되는데 왜 되는지 모르게뜸
# @login_required
# def comment_delete(request, post_id):
#     comment = Comment.objects.get(id=post_id)
#     comment.delete()
#     return redirect("posts:list")

# 수정전코드
# @login_required
# def like(request):
#     user = request.user
#     post = Post.objects.get(id=id)
#     likes = post.like_set.all()
#     check = 0
#     for like in likes:
#         if user == like.user:
#             check = 1
#             like_post = like
#     if check == 1:
#         like_post.delete()
#     else:
#         like = Like(user=user, post=post)
#         like.save()
#     return redirect('posts:list')

@login_required
def like(request,id):
    # 현재 로그인한 사람의 정보
    user = request.user
    # 게시물
    post = Post.objects.get(id=id)
    # 사용자가 좋아요를 눌렀다면(사용자가 좋아요 목록에 있니?)
    if user in post.likes.all():
        post.likes.remove(user)
    # 사용자가 좋아요를 누르지 않았다면
    else:
        post.likes.add(user)
    return redirect('posts:list')