# gameapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 사용자 측
    path('', views.nickname_input, name='nickname_input'),  # 별명 입력 폼
    path('submit/', views.nickname_submit, name='nickname_submit'),  # 별명 입력 처리 후 리다이렉트
    path('in-game/', views.in_game, name='in_game'),  
    
    # 관리자 측
    path('system/control/', views.admin_control, name='admin_control'),
    path('system/stop-input/', views.stop_input, name='stop_input'),
    path('system/start-input/', views.start_input, name='start_input'),

    path('api/game-state/', views.game_state_api, name='game_state_api'),
    path('api/nickname-count/', views.nickname_count_api, name='nickname_count_api'),
]
