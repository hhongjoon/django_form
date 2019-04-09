from django.shortcuts import render, redirect, get_object_or_404
from .models import Board
from .forms import BoardForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    boards = Board.objects.order_by('-pk')
    context={
        'boards':boards
        
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
    context={
        'board':board
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