from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .forms import PostForm, LoginForm, CommentForm
from .models import Post, User, Comment
from django.db import models


# Create your views here.

# 访问localhost:8000/comments/login
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            t = User.objects.filter(username=username)
            user = User(username=username)  # 如果用户名不存在,注册保存用户,否则就使用用户
            if len(t):
                user = User.objects.get(username=username)
            else:
                user.save()
            request.session['is_login'] = True
            request.session['user_id']  = user.id
            request.session['username'] = user.username
            return redirect('/comments/index/')  # 保存session后跳转到/comments/index/
    return render(request, 'login.html')


# 访问localhost:8000/comments/index/由这个视图函数处理
# 　主界面，发布post,查看其他人的post
def index(request):
    is_login = request.session.get('is_login', False)
    if is_login is False:  # 如果没有登录,跳转到登录界面
        return redirect('/comments/login/')
    if is_login:  # 如果已经登录
        # 如果表单提交合法,那么保存到数据库中，然后重定向到当前页面
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                body = form.cleaned_data['body']
                user_id = request.session.get('user_id')
                username = request.session.get('username')
                user = User(username=username, id=user_id)
                post = Post(body=body, author=user)
                post.save()  # 将表单中的数据提取出来,并且存储到数据库中
                return redirect('/comments/index/')
        posts = Post.objects.all()  # 注意:这里是显示所有的动态页面:
        #return HttpResponse(to_json(posts),content_type='application/json')
        return render(request, 'index.html', {'form': request.session.get('username'), 'posts': posts, })


# 访问 localhost:8000/comments/post/1
# 为每一个post分配一个固定链接,也就是唯一的url引用
# 评论这个post
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            author = User.objects.get(id=request.session.get('user_id'))
            post = Post.objects.get(id=post_id)
            Comment.objects.create(body=body, author=author, post=post)  # 创建并保存
            return redirect('/comments/post/' + str(post_id))  # 重定向到当前页面，防止刷新
    comments = Comment.objects.filter(post__id=post_id).select_related()  # 找到所有当前post下的评论
    return render(request, 'post.html', {'post': post, 'comments': comments, 'post_id': post_id})


# 访问 localhost:8000/comments/edit/1
# 编辑编号为post_id的post
def edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.session.get('user_id') == post.author.id:  # 如果文章是当前用户的
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post.body = form.cleaned_data['body']
                post.save()
        return render(request, 'edit_post.html', {'post': post})
    else:  # 文章不属于当前用户,显示没有权限修改
        return HttpResponse('Sorry,You have no the access to modify it!')




def get_friend_news(request):
    posts=Post.objects.all()
    # object_to_json
    obj=[]
    for post in posts:
        #-union-
        union={}
        #--user--
        user={}
        user["userID"]=post.author.id
        user["Nick"]=post.author.username
        #--news--
        news={}
        news["content"]=post.body
        news["NewsID"]=post.id
        news["date"]="2018/06/23 14:57"
        news["cntlike"]=0
        news["liked"]=False
        news_comment=[]
        comments = Comment.objects.filter(post__id=post.id).select_related()  # 找到所有当前post下的评论

        for comment in comments:
            d={}
            d["userID"]=comment.author.id
            d["Nick"]=comment.author.username
            d["commentID"]=comment.id
            d["content"]=comment.body
            news_comment.append(d)
        news["comment"]=news_comment

        union["user"]=user
        union["News"]=news
        obj.append(union)
    return JsonResponse(obj,safe=False)
    #return HttpResponse(serializers.serialize('json',obj),content_type='application/json')
    #return HttpResponse(to_json(posts),content_type='application/json')


def follow(request,user_id):
    if not request.session.get("is_login"):
        return redirect("/comments/index/")
    return HttpResponse('you are now in follow')


def register(request):
    return render(request, 'register.html')


def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect("/comments/login/")


def to_json(obj):
    return serializers.serialize('json', obj)
