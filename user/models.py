import os, random, string, time
from django.db import models
from django.contrib.auth.models import AbstractUser
import os.path
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
def get_profile_image_filepath(self, filename):
    img_path = 'static/upload/user/{0}/avatar.png'.format(self.id)
    if os.path.exists(img_path):
        os.remove(img_path)
    return img_path

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_default_profile_image():
    return "static/img/brand/logo.png"


def get_background_image_filepath(self, filename):
    img_bg_path = 'static/upload/user/{0}/background.png'.format(self.id.id)
    if os.path.exists(img_bg_path):
        os.remove(img_bg_path)
    return img_bg_path


def get_music_filepath(self, filename):
    music_path = 'static/upload/user/{0}/music.mp3'.format(self.id.id)
    if os.path.exists(music_path):
        os.remove(music_path)
    return music_path

class Users(AbstractUser):
    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=30, unique=True, error_messages={
        'required': _("Tên không được để trống"),
        'unique': _("Tên đã được người khác sử dụng."),
        'max_length': _("Tên tối đa 30 kí tự."),
    })
    email = models.EmailField(_('email address'), max_length=50, unique=True, error_messages={
        'required': _("Email không được để trống"),
        'unique': _("Email này đã có người sử dụng."),
        'max_length': _("Email tối đa 50 kí tự.")
    })
    pwd2 = models.CharField(max_length=6, default=id_generator)
    email_verified_at = models.BooleanField(default=False)
    level = models.IntegerField(default=10)
    vip_time = models.IntegerField(null=True, default=0)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                      default=get_default_profile_image)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    def display_level(self):
        context = {}
        level = self.level
        if level == 0:
            context['level_name'] = 'Creator'
            context['buff_level'] = '200%'
            context['user_css'] = 'anh_nhieu_mau'
            context['vip_time'] = None
        elif level == 1:
            context['level_name'] = 'Admin'
            context['buff_level'] = '150%'
            context['user_css'] = 'anh_do1'
            context['vip_time'] = None
        elif level == 2:
            context['level_name'] = 'Mod'
            context['buff_level'] = '100%'
            context['user_css'] = 'anh_tim2'
            context['vip_time'] = None
        elif level == 3:
            context['level_name'] = 'Vip'
            context['buff_level'] = '50%'
            context['user_css'] = 'mau_do'
            context['vip_time'] = None
        elif level == 4:
            context['level_name'] = 'Vip'
            context['buff_level'] = '50%'
            context['user_css'] = 'mau_do'
            context['vip_time'] = time.strftime('%H:%M:%S %d-%m-%Y', time.gmtime(self.vip_time))
        else:
            context['level_name'] = 'Member'
            context['buff_level'] = '10%'
            context['user_css'] = None
            context['vip_time'] = None
        return context

class Profile(models.Model):
    id = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,        
        unique=True,
        primary_key=True
    )
    background_image = models.ImageField(max_length=255, upload_to=get_background_image_filepath, null=True, blank=True)
    name_music = models.CharField(max_length=30, null=True, blank=True)
    url_music = models.FileField(max_length=255, null=True, blank=True, upload_to=get_music_filepath)
    des = models.CharField(max_length=255, null=True, blank=True)
    game_lv = models.IntegerField(default=0)
    game_lv_percent = models.IntegerField(default=0)
    dong_te = models.FloatField(default=5000)
    ngan_te = models.FloatField(default=0)
    kim_te = models.FloatField(default=0)
    m_e = models.FloatField(default=0)
    cong_duc = models.FloatField(default=0)

    def __unicode__(self):
        return self.des
    
class PathUser(models.Model):
    id = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        primary_key=True,
        unique=True,
    )
    dang_doc = models.FileField(max_length=255, null=True, blank=True)
    tu_truyen = models.FileField(max_length=255, null=True, blank=True)
    log = models.FileField(max_length=255, null=True, blank=True)
    game = models.FileField(max_length=255, null=True, blank=True)
    tui_do = models.FileField(max_length=255, null=True, blank=True)
    thanh_tuu = models.FileField(max_length=255, null=True, blank=True)
    ky_nang = models.FileField(max_length=255, null=True, blank=True)
    tieu_phi = models.FileField(max_length=255, null=True, blank=True)
    binh_luan = models.FileField(max_length=255, null=True, blank=True)
    
    def check_path_user(self):
        id = self.id.id
        dang_doc = 'static/upload/user/{0}/{1}'.format(id, 'dang_doc.json')
        if os.path.exists(dang_doc) == False:
            os.makedirs(os.path.dirname(dang_doc), exist_ok=True)
            f = open(dang_doc, 'w')
            self.dang_doc = dang_doc
        if self.dang_doc != dang_doc:
            self.dang_doc = dang_doc
        tu_truyen = 'static/upload/user/{0}/{1}'.format(id, 'tu_truyen.json')
        if os.path.exists(tu_truyen) == False:
            os.makedirs(os.path.dirname(tu_truyen), exist_ok=True)
            f = open(tu_truyen, 'w')
            self.tu_truyen = tu_truyen
        if self.tu_truyen != tu_truyen:
            self.tu_truyen = tu_truyen
        log = 'static/upload/user/{0}/{1}'.format(id, 'log.json')
        if os.path.exists(log) == False:
            os.makedirs(os.path.dirname(log), exist_ok=True)
            f = open(log, 'w')
            self.log = log
        if self.log != log:
            self.log = log
        game = 'static/upload/user/{0}/{1}'.format(id, 'game.json')
        if os.path.exists(game) == False:
            os.makedirs(os.path.dirname(game), exist_ok=True)
            f = open(game, 'w')
            self.game = game
        if self.game != game:
            self.game = game
        tui_do = 'static/upload/user/{0}/{1}'.format(id, 'tui_do.json')
        if os.path.exists(tui_do) == False:
            os.makedirs(os.path.dirname(tui_do), exist_ok=True)
            f = open(tui_do, 'w')
            self.tui_do = tui_do
        if self.tui_do != tui_do:
            self.tui_do = tui_do
        thanh_tuu = 'static/upload/user/{0}/{1}'.format(id, 'thanh_tuu.json')
        if os.path.exists(thanh_tuu) == False:
            os.makedirs(os.path.dirname(thanh_tuu), exist_ok=True)
            f = open(thanh_tuu, 'w')
            self.thanh_tuu = thanh_tuu
        if self.thanh_tuu != thanh_tuu:
            self.thanh_tuu = thanh_tuu
        ky_nang = 'static/upload/user/{0}/{1}'.format(id, 'ky_nang.json')
        if os.path.exists(ky_nang) == False:
            os.makedirs(os.path.dirname(ky_nang), exist_ok=True)
            f = open(ky_nang, 'w')
            self.ky_nang = ky_nang
        if self.ky_nang != ky_nang:
            self.ky_nang = ky_nang
        tieu_phi = 'static/upload/user/{0}/{1}'.format(id, 'tieu_phi.json')
        if os.path.exists(tieu_phi) == False:
            os.makedirs(os.path.dirname(tieu_phi), exist_ok=True)
            f = open(tieu_phi, 'w')
            self.tieu_phi = tieu_phi
        if self.tieu_phi != tieu_phi:
            self.tieu_phi = tieu_phi
        binh_luan = 'static/upload/user/{0}/{1}'.format(id, 'binh_luan.json')
        if os.path.exists(binh_luan) == False:
            os.makedirs(os.path.dirname(binh_luan), exist_ok=True)
            f = open(binh_luan, 'w')
            self.binh_luan = binh_luan
        if self.binh_luan != binh_luan:
            self.binh_luan = binh_luan
        self.save()


#friend
class FriendList(models.Model):

	user 				= models.OneToOneField(Users, on_delete=models.CASCADE, related_name="user")
	friends 			= models.ManyToManyField(Users, blank=True, related_name="friends") 

	def __str__(self):
		return self.user.name

	def add_friend(self, account):
		"""
		Add a new friend.
		"""
		if not account in self.friends.all():
			self.friends.add(account)
			self.save()

	def remove_friend(self, account):
		"""
		Remove a friend.
		"""
		if account in self.friends.all():
			self.friends.remove(account)

	def unfriend(self, removee):
		"""
		Initiate the action of unfriending someone.
		"""
		# Remove friend from remover friend list
		self.remove_friend(removee)

		# Remove friend from removee friend list
		friends_list = FriendList.objects.get(user=removee)
		friends_list.remove_friend(self.user)


	def is_mutual_friend(self, friend):
		"""
		Is this a friend?	
		"""
		if friend in self.friends.all():
			return True
		return False


class FriendRequest(models.Model):
	"""
	A friend request consists of two main parts:
		1. SENDER
			- Person sending/initiating the friend request
		2. RECIVER
			- Person receiving the friend friend
	"""

	sender 				= models.ForeignKey(Users, on_delete=models.CASCADE, related_name="sender")
	receiver 			= models.ForeignKey(Users, on_delete=models.CASCADE, related_name="receiver")

	is_active			= models.BooleanField(blank=False, null=False, default=True)

	timestamp 			= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.name

	def accept(self):
		"""
		Accept a friend request.
		Update both SENDER and RECEIVER friend lists.
		"""
		receiver_friend_list = FriendList.objects.get(user=self.receiver)
		if receiver_friend_list:
			receiver_friend_list.add_friend(self.sender)
			sender_friend_list = FriendList.objects.get(user=self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.delete()

	def decline(self):
		"""
		Decline a friend request.
		Is it "declined" by setting the `is_active` field to False
		"""
		self.delete()


	def cancel(self):
		"""
		Cancel a friend request.
		Is it "cancelled" by setting the `is_active` field to False.
		This is only different with respect to "declining" through the notification that is generated.
		"""
		self.delete()
