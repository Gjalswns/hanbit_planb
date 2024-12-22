# gameapp/models.py
from django.db import models

class GameState(models.Model):
    """
    - 현재 입력이 열려 있는지(open) 여부
    - 게임이 진행 중인지 여부(또는 다른 상태값)를 확장할 수도 있음
    """
    is_open = models.BooleanField(default=True)  # True면 별명 입력 허용

    def __str__(self):
        # 여러 개 GameState가 생기지 않도록 단일 인스턴스만 운영할 수도 있음
        return f"GameState(open={self.is_open})"


class Nickname(models.Model):
    """
    - 입력받은 별명 저장
    """
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
