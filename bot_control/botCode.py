def botCore():
	import telepot
	from django.conf import settings
	return telepot.Bot(settings.BOT_TOKEN)
def ChannelCore():
	from pytg import Telegram
	tg = Telegram(telegram="../Cli/tg/bin/telegram-cli", pubkey_file="../Cli/tg/tg-server.pub")
	return tg.sender
def sendChannel(text):
	sender = ChannelCore()
	sender.msg('U2eet', text)
def sendMessage(chat_id, text):
	return botCore().sendMessage(chat_id, text)
def handleMessage(msg):
	from .models import User
	from django.utils import timezone
	first_name = msg['from']['first_name']
	chat_id = msg['from']['id']
	last_name = '' 
	if 'last_name' in msg['from'].keys():
		last_name = msg['from']['last_name']
	username = '' 
	if 'username' in msg['from'].keys():
		username = msg['from']['username']
	user = User.objects.filter(chat_id = chat_id)
	has = False
	if not user:
		user = User(chat_id = chat_id, first_name = first_name)
	else:
		user = user[0]
		has = True
	user.first_name = first_name
	if last_name:
		user.last_name = last_name
	if username:
		user.username = username
	user.save()
	print(msg)

	if 'text' in msg.keys() and msg['text'] == '/start':
		if not has:
			sendMessage(user.chat_id, 'خوش آمدید :)')
		if not user.nickname:
			sendMessage(user.chat_id, 'نام مستعارتو وارد کن')
		else:
			sendMessage(user.chat_id, 'که چی')
	elif not user.nickname:
		if not 'text' in msg.keys():
			sendMessage(user.chat_id, 'هنوز اسم انتخاب نکردی! اسمتو بنویس')
		elif len(msg['text']) > 30:
			sendMessage(user.chat_id, '۳۰ کاراکتر بیشتر نشه')
		else:
			ls = User.objects.filter(nickname = msg['text'])
			if ls:
				sendMessage(user.chat_id, 'این اسم قبلا انتخاب شده!')
			else:
				user.nickname = msg['text']
				user.save()
				sendMessage(user.chat_id, 'رواله :))')
				sendMessage(user.chat_id, 'از الان میتونی توییت بذاری :)')
	elif not 'text' in msg.keys():
		sendMessage(user.chat_id, 'ناموصا متن بفرست')
	elif 'edit_date' in msg.keys():
		sendMessage(user.chat_id, 'حالا هی تو ادیت کن! هیچی نمیشه')
	elif len(msg['text']) > 300:
		sendMessage(user.chat_id, 'بیشتر از ۳۰۰ تا کاراکتر نمیتونی بفرستی :پی')
	elif int((timezone.now() - user.last_activity).total_seconds()) > 10 or user.tweet_counter == 0:
		sendChannel(msg['text'] + '\n\n' + '#__' + user.nickname + '__' + '\n' + '@U2eet')
		user.new_tweet()
		sendMessage(user.chat_id, 'توییت شما با موفقیت داستان شد ^_^')
	else:
		sendMessage(user.chat_id, 'یه نیم ساعت صبر کن دیگه')
def initBot():
	from telepot.loop import MessageLoop
	print("Initialize Bot ...")
	MessageLoop(botCore(), handleMessage).run_as_thread()
