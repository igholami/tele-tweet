from django.apps import AppConfig

class BotControlConfig(AppConfig):
	name = 'bot_control'
	def ready(self):
		from .botCode import initBot
		initBot()
		print("TelegramBot is active now!")
