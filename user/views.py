import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from user.utils import get_friend_request_or_false
from user.friend_request_status import FriendRequestStatus
from .models import FriendList, FriendRequest

from user.models import Profile, PathUser, Users
from user.forms import UsersCreationFrom, UserUpdateForm, ProfileUpdateForm
from book.models import Book
# Create your views here.

class UserBrowser:
    def check_profile(request):
        data_user = Users.objects.all()
        txt = ""
        for user_data in data_user:
            id = user_data.pk
            try:
                profile = Profile.objects.get(pk=id)
                txt = 'Đã check xong'
            except:
                profile = Profile.objects.create(pk=id)
                profile.save()
                txt += 'Đã check profile<br>'
            try:
                check_path = PathUser.objects.get(pk=id)
                txt = 'Đã check xong'
            except:
                try:
                    check_path = PathUser.objects.create(pk=id)
                    check_path.save()
                except:                    
                    check_path = PathUser.objects.get(pk=id)
                txt += 'Đã check path'                
            check_path.check_path_user()
        return HttpResponse(txt)

    def register(request):
        form = UsersCreationFrom()
        if request.user.is_authenticated:
            return redirect('/')
        if request.method == 'POST':
            form = UsersCreationFrom(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                UserBrowser.check_profile(request)
                messages.success(request, 'Đã tạo tài khoản với email ' + email)
                return redirect('login')
        context = {'form': form}
        return render(request, 'auth/register.html', context)

    def home(request):
        context = {}
        context['update'] = Book.objects.all().order_by('-date_update')[:12]
        return render(request, 'home/index.html', context)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'auth/password/forgot_password.html'
    email_template_name = 'auth/password/email_form_rspwd.html'
    subject_template_name = 'auth/password/password_reset_subject.txt'
    success_message = "Chúng tôi đã gửi cho bạn hướng dẫn về cách đặt lại mật khẩu của bạn qua email, " \
                      "nếu tài khoản tồn tại với email bạn đã nhập. Bạn sẽ sớm nhận được chúng." \
                      " Nếu bạn không nhận được email, " \
                      "hãy đảm bảo rằng bạn đã nhập địa chỉ mà bạn đã đăng ký và kiểm tra thư mục spam của bạn."
    success_url = reverse_lazy('home')


class ProfileBrowser:
    @login_required(login_url='/login/')
    def my_profile(request):
        context = {}
        user_id = request.user.id
        if not request.user.is_authenticated:
            return redirect('/login/')
        try:
            user_data = Users.objects.get(pk=user_id)
            profile_data = Profile.objects.get(pk=user_id)
        except:
            return HttpResponse("<center>Không tìm thấy người dùng.<center>")
        if user_data and profile_data:
            context['id'] = user_data.id
            context['name'] = user_data.name
            context['date_joined'] = user_data.date_joined
            context['profile_image'] = user_data.profile_image
            context['background_image'] = profile_data.background_image
            context['name_music'] = profile_data.name_music
            context['url_music'] = profile_data.url_music
            context['des'] = profile_data.des
            context['dong_te'] = profile_data.dong_te
            context['ngan_te'] = profile_data.ngan_te
            context['kim_te'] = profile_data.kim_te
            context['m_e'] = profile_data.m_e
            
            level_data = user_data.display_level()
            context['level_name'] = level_data['level_name']
            context['buff_level'] = level_data['buff_level']
            context['user_css'] = level_data['user_css']
            context['vip_time'] = level_data['vip_time']
            
            try:
                friend_list = FriendList.objects.get(user=user_data)
            except FriendList.DoesNotExist:
                friend_list = FriendList(user=user_data)
                friend_list.save()
            friends = friend_list.friends.all()
            context['friends'] = friends
                
            # Set the template variables to the values
            user = request.user
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass
            context['friend_requests'] = friend_requests
        return render(request, 'auth/profile/auth.html', context)

    def guest_profile(request, *args, **kwargs):
        context = {}
        try:
            user_id = kwargs.get('user_id')
            user_data = Users.objects.get(pk=user_id)
            profile_data = Profile.objects.get(pk=user_id)
        except:
            return HttpResponse("Người dùng không tồn tại.")
        if user_data and profile_data:
            context['id'] = user_data.id
            context['name'] = user_data.name
            context['date_joined'] = user_data.date_joined
            context['profile_image'] = user_data.profile_image
            context['background_image'] = profile_data.background_image
            context['name_music'] = profile_data.name_music
            context['url_music'] = profile_data.url_music
            context['des'] = profile_data.des
            
            level_data = user_data.display_level()
            context['level_name'] = level_data['level_name']
            context['buff_level'] = level_data['buff_level']
            context['user_css'] = level_data['user_css']
            context['vip_time'] = level_data['vip_time']
                
            try:
                friend_list = FriendList.objects.get(user=user_data)
            except FriendList.DoesNotExist:
                friend_list = FriendList(user=user_data)
                friend_list.save()
            friends = friend_list.friends.all()
            context['friends'] = friends
            # Define template variables
            is_self = True
            is_friend = False
            request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
            friend_requests = None
            user = request.user
            if user.is_authenticated and user != user_data:
                is_self = False
                if friends.filter(pk=user.id):
                    is_friend = True
                else:
                    is_friend = False
                    # CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
                    if get_friend_request_or_false(sender=user_data, receiver=user) != False:
                        request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                        context['pending_friend_request_id'] = get_friend_request_or_false(sender=user_data, receiver=user).id
                    # CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
                    elif get_friend_request_or_false(sender=user, receiver=user_data) != False:
                        request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                        context['pending_friend_request_id'] = get_friend_request_or_false(sender=user, receiver=user_data).id
                    # CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
                    else:
                        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
            
            elif not user.is_authenticated:
                is_self = False
            else:
                try:
                    friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
                except:
                    pass
                
            # Set the template variables to the values
            context['is_self'] = is_self
            context['is_friend'] = is_friend
            context['request_sent'] = request_sent
            context['friend_requests'] = friend_requests
        return render(request, 'auth/profile/guest.html', context)
    
    @login_required(login_url='/login/')
    def edit_profile(request):
        context = {}
        user_id = request.user.id
        try:
            user_data = Users.objects.get(pk=user_id)
            profile_data = Profile.objects.get(pk=user_id)
        except:
            return HttpResponse(
                "<center>Tài khoản của bạn bị lỗi vui lòng load lại trang hoặc liên hệ admin để được hỗ "
                "trợ.<center>")
        if user_data:
            context['id'] = user_data.id
            context['name'] = user_data.name
            context['date_joined'] = user_data.date_joined
            context['profile_image'] = user_data.profile_image
            context['background_image'] = profile_data.background_image
            context['name_music'] = profile_data.name_music
            context['url_music'] = profile_data.url_music
            context['des'] = profile_data.des
            context['ngan_te'] = profile_data.ngan_te
        return render(request, 'auth/profile/edit.html', context)

    @login_required(login_url='/login/')
    def edit_account(request):
        user_id = request.user.id
        try:
            user_data = Users.objects.get(pk=user_id)
            profile_data = Profile.objects.get(pk=user_id)
        except:
            return HttpResponse("<center>Không tìm thấy người dùng.<center>")
        if user_data.pk != request.user.pk:
            return HttpResponse("Bạn không thể sửa thông tin của người khác.")
        context = {}
        if request.POST:
            ngan_te = 0

            if not request.POST['name']:
                messages.error(request, 'Bạn không muốn đổi tên thì để im ô tên nhé.')
                return redirect("my_profile")
            else:
                if request.user.name != request.POST['name']:
                    try:
                        account = Users.objects.exclude(pk=user_id).get(name=request.POST['name'])
                        messages.error(request, 'Tên %s đã có người dùng.' % request.POST['name'])
                        return redirect("my_profile")
                    except Users.DoesNotExist:
                        ngan_te = ngan_te + 1000

            try:
                profile_image = request.FILES['profile_image']
                if profile_image.size > settings.MAX_UPLOAD_SIZE:
                    messages.error(request, 'Ảnh phải nhỏ hơn 1MB.')
                    return redirect("my_profile")
                ngan_te = ngan_te + 1000
            except:
                ngan_te = ngan_te + 0

            try:
                background_image = request.FILES['background_image']
                if background_image.size > settings.MAX_UPLOAD_SIZE:
                    messages.error(request, 'Ảnh phải nhỏ hơn 1MB.')
                    return redirect("my_profile")
                ngan_te = ngan_te + 1000
            except:
                ngan_te = ngan_te + 0

            try:
                url_music = request.FILES['url_music']
                if url_music.size > 5242880:
                    messages.error(request, 'File nhạc nhỏ hơn 5MB.')
                    return redirect("my_profile")
                ngan_te = ngan_te + 1000
            except:
                ngan_te = ngan_te + 0

            try:
                name_music = request.POST['name_music']
                if len(name_music) > 30:
                    messages.error(request, 'Tên nhạc không quá 30 kí tự')
            except:
                ngan_te = ngan_te + 0

            try:
                des = request.POST['des']
                if len(des) > 255:
                    messages.error(request, 'Giới thiệu không quá 255 khí tự.')
            except:
                ngan_te = ngan_te + 0

            if profile_data.ngan_te < ngan_te:
                messages.error(request, 'Bạn không đủ ngân tệ để đổi thông tin.')
                return redirect("my_profile")

            profile_instance = get_object_or_404(Profile, pk=request.user)
            form = UserUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
            form_profile = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile_instance)

            if all([form.is_valid(), form_profile.is_valid()]):
                parent = form.save(commit=False)
                parent.save()
                child = form_profile.save(commit=False)
                child.save()
            try:
                data_profile = Profile.objects.get(pk=user_id)
                crr_ngan_te = profile_data.ngan_te - ngan_te
                data_profile.ngan_te = crr_ngan_te
                data_profile.save()
                messages.success(request, "Đã đổi thông tin thành công. Mất %s ngân tệ." % ngan_te)
                return redirect("my_profile")
            except:
                messages.error(request, "Lỗi trừ ngân tệ.")
                return redirect("my_profile")
        messages.error(request, 'Có lỗi xảy ra')
        return redirect("my_profile")

    def menu_profile(request):
        return render(request, 'auth/profile/menu.html')


#friend
def friends_list_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
		if user_id >= 0:
			try:
				this_user = Users.objects.get(pk=user_id)
				context['this_user'] = this_user
			except Users.DoesNotExist:
				return HttpResponse("Người dùng đó không tồn tại.")
			try:
				friend_list = FriendList.objects.get(user=this_user)
			except FriendList.DoesNotExist:
				return HttpResponse(f"Không thể tìm thấy danh sách bạn bè cho {this_user.name}")
			
			# Must be friends to view a friends list
			if user != this_user:
				if not user in friend_list.friends.all():
					return HttpResponse("Bạn phải là bạn bè để xem danh sách bạn bè của họ.")
			friends = [] # [(friend1, True), (friend2, False), ...]
			# get the authenticated users friend list
			auth_user_friend_list = FriendList.objects.get(user=this_user)
			for friend in friend_list.friends.all():
				friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
			context['friends'] = friends
	else:		
		return HttpResponse("Bạn phải là bạn bè để xem danh sách bạn bè của họ.")
	return render(request, "friend/friend_list.html", context)

def list_friend_request(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
        context['friend_requests'] = friend_requests
    else:
        return HttpResponse("<center>Vui lòng đăng nhập để tiếp tục.<center>")
    return render(request, "friend/friend_requests.html", context)

def send_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = Users.objects.get(pk=user_id)
			try:
				# Get any friend requests (active and not-active)
				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
				# find if any of them are active (pending)
				try:
					for request in friend_requests:
						if request.is_active:
							raise Exception("You already sent them a friend request.")
					# If none are active create a new friend request
					friend_request = FriendRequest(sender=user, receiver=receiver)
					friend_request.save()
					payload['response'] = "Friend request sent."
				except Exception as e:
					payload['response'] = str(e)
			except FriendRequest.DoesNotExist:
				# There are no friend requests so create one.
				friend_request = FriendRequest(sender=user, receiver=receiver)
				friend_request.save()
				payload['response'] = "Friend request sent."

			if payload['response'] == None:
				payload['response'] = "Something went wrong."
		else:
			payload['response'] = "Unable to sent a friend request."
	else:
		payload['response'] = "You must be authenticated to send a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")

def accept_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			# confirm that is the correct request
			if friend_request.receiver == user:
				if friend_request: 
					# found the request. Now accept it
					updated_notification = friend_request.accept()
					payload['response'] = "Done."

				else:
					payload['response'] = "Có lỗi xảy ra."
			else:
				payload['response'] = "Đó không phải là yêu cầu của bạn để chấp nhận."
		else:
			payload['response'] = "Không thể chấp nhận yêu cầu kết bạn đó."
	else:
		# should never happen
		payload['response'] = "Bạn phải đăng nhập để chấp nhận yêu cầu kết bạn."
	return HttpResponse(json.dumps(payload), content_type="application/json")

def remove_friend(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		user_id = kwargs.get("receiver_user_id")
		if user_id is not None:
			try:
				friend_list = FriendList.objects.get(user=user)
				removee = Users.objects.get(pk=user_id)
			except Exception as e:
				payload['response'] = f"Có lỗi xảy ra: {str(e)}"			
			if removee is not None or friend_list.is_mutual_friend(removee) == True:
				try:
					friend_list.unfriend(removee)
					payload['response'] = "Done."
				except Exception as e:
					payload['response'] = f"Có lỗi xảy ra: {str(e)}"
			else:
				payload['response'] = "Có một lỗi. Không thể xóa người bạn đó."
		else:
			payload['response'] = "Không thể xóa người bạn đó."
	else:
		# should never happen
		payload['response'] = "Bạn phải đăng nhập để xóa một người bạn."
	return HttpResponse(json.dumps(payload), content_type="application/json")

def decline_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			# confirm that is the correct request
			if friend_request.receiver == user or friend_request.sender == user:
				if friend_request: 
					# found the request. Now decline it
					updated_notification = friend_request.decline()
					payload['response'] = "Done."
				else:
					payload['response'] = "Có lỗi xảy ra."
			else:
				payload['response'] = "Không cần làm hộ người khác."
		else:
			payload['response'] = "Không thể từ chối yêu cầu kết bạn đó."
	else:
		# should never happen
		payload['response'] = "Bạn phải đăng nhập để xóa một người bạn."
	return HttpResponse(json.dumps(payload), content_type="application/json")