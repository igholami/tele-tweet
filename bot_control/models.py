from django.db import models
import telepot
from django.utils import timezone

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=30, blank=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30, blank=True)
	chat_id = models.IntegerField()
	is_admin = models.BooleanField(default=False)
	last_activity = models.DateTimeField(default=timezone.now)
	tweet_counter = models.IntegerField(default=0)
	nickname = models.CharField(max_length=30, default='', blank=True)
	def __str__(self):
		return self.first_name + " - " + self.username
	def save(self, *args, **kwargs):
		super(User, self).save(*args, **kwargs)
	def new_tweet(self, *args, **kwargs):
		self.last_activity = timezone.now()
		self.tweet_counter += 1
		self.save()
		
class Channel(models.Model):
	text = models.CharField(max_length=3000)
	time = models.DateTimeField(default=timezone.now)
	new = True
	def __str__(self):
		return self.text
	def save(self, *args, **kwargs):
		print(self.pk, end=' -------\n')
		tmp = self.pk
		super(Channel, self).save(*args, **kwargs)
		for user in User.objects.all():
			if tmp is None:
				new = Message(user = user, channel = self)
				new.save()
			else:
				A = Message.objects.filter(user = user, channel = self)
				for a in A:
					a.edit()
		self.new = False

class Message(models.Model):
	message_id = models.IntegerField(default = -1)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
	def __str__(self):
		return self.channel.text + ' - ' + self.user.first_name
	def save(self, *args, **kwargs):
		from .botCode import botCore
		import telepot
		Bot = botCore()
		response = Bot.sendMessage(self.user.chat_id, self.channel.text)
		print(response);
		self.message_id = response['message_id']
		super(Message, self).save(*args, **kwargs)

	def edit(self):
		from .botCode import botCore
		import telepot
		Bot = botCore()
		Bot.editMessageText((self.user.chat_id, self.message_id), self.channel.text)	
		
