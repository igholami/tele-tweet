from django.contrib import admin
from .models import User, Channel, Message

# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display = ['username', 'first_name', 'last_name', 'nickname', 'chat_id', 'is_admin', 'last_activity']
admin.site.register(User, UserAdmin)

class MessageInline(admin.StackedInline):
	model = Message
class ChannelAdmin(admin.ModelAdmin):
	list_display = ['text', 'time']
	inlines = [MessageInline]
admin.site.register(Channel, ChannelAdmin)
class MessageAdmin(admin.ModelAdmin):
	pass
admin.site.register(Message, MessageAdmin)
