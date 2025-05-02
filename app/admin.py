from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')  
    list_filter = ('created_at', 'updated_at') 
    search_fields = ('user__username',)  
    readonly_fields = ('created_at', 'updated_at')  
