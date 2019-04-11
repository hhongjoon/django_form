from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_POST
# import hashlib # 암호화시켜줌

from .models import Board, Comment
from .forms import BoardForm, CommentForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    
    # if request.user.is_authenticated:
    #     gravatar_url = hashlib.md5(request.user.email.strip().lower().encode('utf-8')).hexdigest()   # 이메일 넘기는 방법, 문서에 나와있음
    # else:
    #     gravatar_url = None
    boards = get_list_or_404(Board.objects.order_by('-pk'))
    # boards = Board.objects.order_by('-pk')
    
    
    context={
        'boards':boards,
        
        # 'gravatar_url':gravatar_url,
    }
    return render(request,'boards/index.html', context)

@login_required    
def create(request):
    
        # 이 처리과정은 'binding'으로 불리는데, 폼의 유효성 체크를 할 수 있도록 해준다.
    form = BoardForm(request.POST)
    if request.method == 'POST':
        # form 유효성 체크
        if form.is_valid():
            # title = request.POST.get('title')
            # title = form.cleaned_data.get('title')     # 
            # content = form.cleaned_data.get('content')
            # # 검증 통과한 깨끗한 데이터를 form에서 가져와서  board를 만든다.
            # board = Board.objects.create(title = title, content=content)
            board = form.save(commit=False)
            # board를 바로 저장하지 않고, 현재 user를 넣고 저장
            # request.user에서 가져와서 그 후에 저장한다.
            board.user = request.user
            
            board.save()                                                  ## 이미 모델이 valid 하므로 이렇게 저장가능
            return redirect('boards:detail', board.pk)
    # Get 또는 다른 메소드일 때, 기본 form을 생성한다.
    else:
        form = BoardForm()

    
    context = {'form':form,
                
    }
    return render(request,'boards/form.html', context)
        
def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    # comments = Comment.objects.filter(board=board_pk).all()
    form = CommentForm()
    context={
        'board':board,
        # 'comments':comments,
        'form':form,
    }
    return render(request, 'boards/detail.html', context)

def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if request.method == 'POST':
            board.delete()
            return redirect('boards:index')
        else:
            return redirect('board:detail', board.pk)
            
    else:
        return redirect('boards:index')
@login_required         
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
    
        if request.method =='POST':
            form = BoardForm(request.POST, instance=board)          #1
            if form.is_valid():
                # board.title = form.cleaned_data.get('title')
                # board.content = form.cleaned_data.get('content')
                # board.save()
                board = form.save()
                    #1
                return redirect('boards:detail', board.pk)
        # GET 요청이면 (수정하기 버튼을 눌렀을 때)
        else:
            # BoardForm을 초기화(사용자 입력 값을 넣어준 상태로)
            
            form = BoardForm(initial=board.__dict__)
            # form = BoardForm(initial={'title':board.title, 'content':board.content})
            
            
        # POST로 넘어왔을때, 검증에 실패한다면 오류 메시지가 포함된 상태
        # GET : 요청에서 초기화된 상태
        
    else: 
        return redirect('boards:index')
    context = {'form':form, 
                'board':board,
    }
    return render(request, 'boards/form.html', context)

@require_POST # get 방식은 들어오지 못함
@login_required
def comment_create(request, board_pk):
    # if request.user.is_authenticated:   # 위에 데코해서 없어도 됨
        
    form = CommentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            
            comment = form.save(commit=False)
            comment.user = request.user # 객체 자체를 넣어준다.
            comment.board_id = board_pk
            comment.save()
                
    return redirect('boards:detail',board_pk)

@require_POST
@login_required
def comment_delete(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, board_id = board_pk)
    
    if request.user == comment.user:
        comment.delete()
    return redirect('boards:detail', board_pk)