from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash

from .forms import UserCustomChangeForm, UserCustomCreationForm

# Create your views here.

def signup(request):
    if request.user.is_authenticated:   # 로그인 상태 확인 user.is_authenticated
        return redirect('boards:index')
    
    if request.method == 'POST':  #  회원가입 했을 때
        form = UserCustomChangeForm(request.POST)
        if form.is_valid():
            user = form.save()  # 폼을 저장하고
            auth_login(request, user)   #  로그인함수를 통해 로그인 바로 진행 -> 로그인 상태로 index로
            return redirect('boards:index')  ## 로그인이 된상태로 넘어간다.
        
    else:
        form = UserCustomCreationForm()
        # 폼만 가져온다.
    context = { 'form': form }
    return render(request, 'accounts/auth_form.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    
    
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.POST.get('next') or 'boards:index')  # or 이기떄문에 'next'를 받으면 boards/new로 넘어간다.
            #  로그인 끝나면 인덱스로
    else:
        form = AuthenticationForm()
    context = {
        'form':form,
        'next' : request.GET.get('next',''),
    }
    return render(request, 'accounts/login.html',context)
    
def logout(request):
    auth_logout(request)
    return redirect('boards:index')

def delete(request):
    user = request.user
    if request.method == 'POST':
        # 삭제시키면 알아서 로그아웃 
        user.delete()
    return redirect('boards:index')
    
def edit(request):
    if request.method =='POST':
        # 수정로직 진행
        form = UserCustomChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
            
    else:
        form = UserCustomChangeForm(instance=request.user)
    context = {'form':form}
    return render(request,'accounts/auth_form.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)  # 순서주의 할 것
        if form.is_valid():
            
            user = form.save()
            update_session_auth_hash(request, user)   # 현재 유저가 로그아웃 되는 것을 막아준다.
            return redirect('boards:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form,}
    return render(request, 'accounts/auth_form.html', context)