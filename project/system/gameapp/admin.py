from django.contrib import admin

# Register your models here.
# gameapp/admin.py
from django.contrib import admin
from .models import GameState, Nickname

@admin.register(GameState)
class GameStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_open')

@admin.register(Nickname)
class NicknameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    ordering = ('-created_at', )
