from django.apps import AppConfig


class BotControlConfig(AppConfig):
    name = "bot_control"

    def ready(self):
        from .bot_code import init_bot

        init_bot()
        print("TelegramBot is active now!")
