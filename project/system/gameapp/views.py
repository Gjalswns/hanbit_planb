# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Nickname, GameState
from django.http import HttpResponse, JsonResponse  # <-- 추가
import csv

def nickname_input(request):
    """
    별명 입력 폼을 보여주는 뷰
    - 만약 관리자에서 입력 중단(is_open=False) 상태라면, 입력 불가
    """
    # 단일 GameState 객체 가져오기 (get() 사용 시 없으면 에러 → try except 처리)
    try:
        game_state = GameState.objects.get(id=1)
    except GameState.DoesNotExist:
        # 초기 상태(테스트용)
        game_state = GameState.objects.create(is_open=True)

    # 만약 입력이 중단된 상태이면, 403 에러 or 다른 페이지로 이동
    if not game_state.is_open:
        return render(request, 'waiting.html')
    
    return render(request, 'nickname_input.html')  # 템플릿 렌더링


def nickname_submit(request):
    """
    POST로 받은 별명을 DB에 저장 후, 특정 HTML 페이지로 리다이렉트
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            # 입력 가능 여부 다시 확인
            game_state = GameState.objects.get(id=1)
            if not game_state.is_open:
                return render(request, 'nickname_input.html')
            
            Nickname.objects.create(name=name)
            
            # 세션(session)에 별명을 저장
            request.session['nickname'] = name

            # in_game 페이지(새로 만든)로 리다이렉트
            return redirect('in_game')
            
    # GET이나 빈 값인 경우, 다시 폼으로 보냄
    return redirect('nickname_input')

def in_game(request):
    """
    in_game 페이지 뷰
    - 세션에서 nickname을 꺼내 템플릿으로 전달
    """
    nickname = request.session.get('nickname', None)
    context = {
        'nickname': nickname
    }
    return render(request, 'in_game.html', context)



######################################################################################

def admin_control(request):
    """
    관리자용 페이지: 전체 별명 리스트 확인 + 버튼
    """
    all_nicknames = Nickname.objects.all().order_by('-created_at')
    game_state = GameState.objects.get(id=1)
    context = {
        'nicknames': all_nicknames,
        'game_state': game_state,
    }
    return render(request, 'admin_control.html', context)


def stop_input(request):
    """
    입력을 중단하고, (게임 시작 가정)
    """
    if request.method == 'POST':
        # 1) 입력 중단 처리
        game_state = GameState.objects.get(id=1)
        game_state.is_open = False
        game_state.save()

        # 2) Nickname 전부 조회
        all_nicknames = Nickname.objects.all()

        # 3) CSV Response 생성
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="nicknames.csv"'

        writer = csv.writer(response)
        # 헤더 없음, 닉네임만 한 줄씩
        for n in all_nicknames:
            writer.writerow([n.name])

        return response
    
    # GET 방식 등 잘못된 접근일 경우 그냥 관리자 페이지로 돌려보냄
    return redirect('admin_control')


def start_input(request):
    """
    입력을 새로 받기 시작 (학번 입력 시작 버튼)
    - 기존 별명 모두 삭제
    - 입력 허용
    """
    if request.method == 'POST':
        Nickname.objects.all().delete()  # 별명 초기화
        game_state = GameState.objects.get(id=1)
        game_state.is_open = True
        game_state.save()
    return redirect('admin_control')

#################################################################################

def game_state_api(request):
    """
    GameState의 is_open 값을 JSON 형태로 반환
    예: {"is_open": true}
    """
    try:
        game_state = GameState.objects.get(id=1)
        return JsonResponse({"is_open": game_state.is_open})
    except GameState.DoesNotExist:
        # 혹은 적절히 처리
        return JsonResponse({"is_open": False})

def nickname_count_api(request):
    """
    닉네임 테이블에 저장된 레코드(인원 수)를 반환
    예: {"count": 5}
    """
    count = Nickname.objects.count()
    return JsonResponse({"count": count})