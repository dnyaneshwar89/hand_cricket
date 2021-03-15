from django.contrib import admin
from .models import LeaderBoard
# Register your models here.

class LeaderBoardAdmin(admin.ModelAdmin):
    list_display = ('id','name','score')
    list_display_links = ('id','name')

admin.site.register(LeaderBoard,LeaderBoardAdmin)
