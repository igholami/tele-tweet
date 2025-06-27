def get_bot_core():
    import telepot
    from django.conf import settings

    return telepot.Bot(settings.BOT_TOKEN)


def get_channel_core():
    from pytg import Telegram
    from django.conf import settings

    tg = Telegram(
        telegram=settings.TELEGRAM_CLI_PATH or "../Cli/tg/bin/telegram-cli",
        pubkey_file=settings.TELEGRAM_PUBKEY_PATH or "../Cli/tg/tg-server.pub",
    )
    return tg.sender


def send_to_channel(text):
    sender = get_channel_core()
    from django.conf import settings

    channel_name = getattr(settings, "TELEGRAM_CHANNEL", "U2eet")
    sender.msg(channel_name, text)


def send_message(chat_id, text):
    return get_bot_core().sendMessage(chat_id, text)


def handle_message(msg):
    from .models import User
    from django.utils import timezone
    from django.utils.translation import gettext as _

    first_name = msg["from"]["first_name"]
    chat_id = msg["from"]["id"]
    last_name = ""
    if "last_name" in msg["from"].keys():
        last_name = msg["from"]["last_name"]
    username = ""
    if "username" in msg["from"].keys():
        username = msg["from"]["username"]
    user = User.objects.filter(chat_id=chat_id)
    user_exists = False
    if not user:
        user = User(chat_id=chat_id, first_name=first_name)
    else:
        user = user[0]
        user_exists = True
    user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if username:
        user.username = username
    user.save()
    print(msg)

    if "text" in msg.keys() and msg["text"] == "/start":
        if not user_exists:
            send_message(user.chat_id, _("Welcome :)"))
        if not user.nickname:
            send_message(user.chat_id, _("Enter your nickname"))
        else:
            send_message(user.chat_id, _("What's up?"))
    elif not user.nickname:
        if "text" not in msg.keys():
            send_message(
                user.chat_id, _("You haven't chosen a name yet! Write your name")
            )
        elif len(msg["text"]) > 30:
            send_message(user.chat_id, _("No more than 30 characters"))
        else:
            existing_nicknames = User.objects.filter(nickname=msg["text"])
            if existing_nicknames:
                send_message(user.chat_id, _("This name has already been chosen!"))
            else:
                user.nickname = msg["text"]
                user.save()
                send_message(user.chat_id, _("Great! :))"))
                send_message(user.chat_id, _("Now you can post tweets :)"))
    elif "text" not in msg.keys():
        send_message(user.chat_id, _("Please send text"))
    elif "edit_date" in msg.keys():
        send_message(user.chat_id, _("Stop editing! Nothing will happen"))
    elif len(msg["text"]) > 300:
        send_message(user.chat_id, _("You cannot send more than 300 characters :P"))
    elif (
        int((timezone.now() - user.last_activity).total_seconds()) > 1800
        or user.tweet_counter == 0
    ):
        from django.conf import settings

        channel_handle = getattr(settings, "TELEGRAM_CHANNEL_HANDLE", "@U2eet")
        send_to_channel(
            msg["text"] + "\n\n" + "#__" + user.nickname + "__" + "\n" + channel_handle
        )
        user.new_tweet()
        send_message(user.chat_id, _("Your tweet was posted successfully ^_^"))
    else:
        send_message(user.chat_id, _("Wait another half hour"))


def init_bot():
    from telepot.loop import MessageLoop

    print("Initialize Bot ...")
    MessageLoop(get_bot_core(), handle_message).run_as_thread()
