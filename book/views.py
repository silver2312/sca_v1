import json
from multiprocessing import context
from .models import Book, Rating
from .extensions import check_url, trans_for_text, trans_author, request_url, get_hostbk, about_bk
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request, host,host_id):
    user = request.user
    context = {}
    appect_host = ['uuxs','writter','convert']
    if not host in appect_host:
        messages.error(request, 'Nguồn này web chưa hỗ trợ nhé.')
        return redirect("home")
    if host == "uuxs":
        url = "https://www.uuxs.com/book/" + str(host_id) + "/"
        bk = Book.objects.filter(url = url).first()
    else:
        bk = Book.objects.filter(id=host_id).filter(url=host).first()
    if not bk:
        messages.error(request, 'Web chưa có truyện này.')
        return redirect("home")
    rt = Rating.tong(bk.id)
    context = {
        'id' : bk.id,
        'title' : bk.title,
        'image_b' : bk.image,
        'author' : bk.author,
        'des' : bk.des,
        'category' : bk.the_loai.all(),
        'tag' : bk.tag.all(),
        'date' : bk.date_update,
        'status' : bk.get_trang_thai_display(),
        'rating' : rt,
        'user_post':bk.user,
        'url': bk.url
    }
    if user.is_authenticated:
        rt_check = Rating.objects.filter(book=bk.id).filter(user=user.id)
        if rt_check:
            context['rt_check'] = 1
        else:
                context['rt_check'] = 0
        
    return render(request, 'book/home.html', context)

@login_required(login_url='/login/')
def search(request):    
    if request.method == "GET":
        key = request.GET['key']
        if check_url(key):
            host = get_hostbk(key)
            appect_host = ['uuxs','writter','convert']
            if not host in appect_host:
                messages.error(request, 'Nguồn này web chưa hỗ trợ nhé.')
                return redirect("home")
            check = Book.objects.filter(url = key).first()
            if check:
                return redirect('book_home',host= host, host_id=key.split("/")[4])
            if host == "uuxs":
                soup = about_bk(key)
                title = soup['title']
                author =soup['author']
                des = soup['des']
            b = Book.objects.create(title= title, author=author, des = des, user=request.user,url=key)
            b.save()
            return redirect('book_home',host= host, host_id=key.split("/")[4])
        else:
            check = Book.objects.all()
            id_b = []
            key_check = key.strip().lower()
            for b in check:
                if ( key_check in trans_for_text(b.title).get_text().lower() ):
                    id_b.append(b.id)
                elif (key_check in trans_author(b.author).get_text().lower() ):
                    id_b.append(b.id)
            book_list = Book.objects.filter(id__in = id_b).order_by('-date_update')
            
            paginator = Paginator(book_list, 12)  
            pageNumber = request.GET.get('page')
            try:
                book = paginator.page(pageNumber)
            except PageNotAnInteger:
                book = paginator.page(1)
            except EmptyPage:
                book = paginator.page(paginator.num_pages)
            return render(request, 'book/list.html', {'book':book,'key':key})
    else:
        return redirect('home')
    
@login_required(login_url='/login/')
def vote(request):
    payload = {}
    user = request.user
    if request.method == 'POST':
        bk_id = request.POST.get('bk_id')
        rate = request.POST.get('rate')
        bk = Book.objects.filter(id=bk_id).first()
        obj = Rating.objects.filter(book=bk_id).filter(user=user.id)
        if bk.trang_thai > 0:
            if obj:
                payload['warring'] = True
            else:
                try:
                    rating = Rating.objects.create(user=user.id,rating=rate,book=bk_id)
                    rating.save()
                    payload['success'] = True
                except:
                    payload['error'] = True
        else:
            payload['check'] = True
    else:
        payload['error'] = True
    return HttpResponse(json.dumps(payload), content_type="application/json")

def de_cu(request):
    context = {}
    context['de_cu'] = Book.objects.filter(de_cu = True).order_by('-date_update')
    return render(request, 'home/caroul.html', context)

def chapter_list(request, bk_id):
    context = {}
    payload = ""
    try:
        bk = Book.objects.filter(id=bk_id).first()
        if bk.trang_thai > 0:
            f = open(bk.chapter.path, encoding='utf-8')
            data = json.load(f)
            length = len(data)
            context['url'] = bk.url
            try:
                bk.get_sub_title()
                payload += "Đã check sub chương truyện "+ trans_for_text(bk.title).get_text()+"<br>"
            except:
                payload += "Có lỗi xảy ra khi check sub chương truyện "+ trans_for_text(bk.title).get_text()+"<br>"
        else:
            data = []
            length = 0
    except:
        data = []
        length = 0
    last_read = 100
    if last_read <= length:
        context['last_read'] = last_read
    else:
        context['last_read'] = 0
    context['data'] = zip(range(length),data)
    return render(request, 'book/chapter_list.html', context)

def data_chap(request,host,host_id,chap_id):
    user = request.user
    context = {}
    appect_host = ['uuxs','writter','convert']
    if not host in appect_host:
        messages.error(request, 'Nguồn này web chưa hỗ trợ nhé.')
        return redirect("home")
    if host == "uuxs":
        url = "https://www.uuxs.com/book/" + str(host_id) + "/"
        bk = Book.objects.filter(url = url).first()
    else:
        bk = Book.objects.filter(id=host_id).filter(url=host).first()
    if not bk:
        messages.error(request, 'Web chưa có truyện này.')
        return redirect("home")
    context['title'] = bk.title
    arr = bk.get_content_id(chap_id)
    if user.is_authenticated:
        context['content'] = arr["content"]
    else:
        context['content'] = "Bạn phải đăng nhập để đọc truyện!"
    context['sub_title'] = arr['sub_title']
    context['author'] = bk.author
    context['user_post'] = bk.user.name
    context['x'] = chap_id
    try:
        f = open(bk.chapter.path ,encoding='utf-8')
        data = json.load(f)
        lenght = len(data)
    except:
        lenght = 0
    max_c = max(range(lenght))
    if chap_id > 0:
        pre_c = chap_id - 1
    else:
        pre_c = -1
    if chap_id < max_c:
        next_c = chap_id + 1
    else:
       next_c = -1
    context['pre_c'] = pre_c
    context['next_c'] = next_c
    context['host'] = host
    context['host_id'] = host_id
    return render(request, 'book/content.html', context)

def check_all(request,id):
    payload = ""
    b = Book.objects.filter(id = id).first()
    if b.trang_thai > 0:
        try:
            b.check_file()
            payload += "Đã check file truyện "+ trans_for_text(b.title).get_text() +"<br>"
        except:
            payload += "Có lỗi xảy ra khi check file truyện "+ trans_for_text(b.title).get_text()+"<br>"
        try:
            b.download_image()
            payload += "Đã check ảnh truyện "+ trans_for_text(b.title).get_text()+"<br>"
        except:
            payload += "Có lỗi xảy ra khi check ảnh truyện "+ trans_for_text(b.title).get_text()+"<br>"
        try:
            b.get_chaplist()
            payload += "Đã check chương truyện "+ trans_for_text(b.title).get_text()+"<br>"
        except:
            payload += "Có lỗi xảy ra khi check chương truyện "+ trans_for_text(b.title).get_text()+"<br>"
    return HttpResponse(payload)
def check_content(request):
    payload = ""
    if request.method == "POST":
        id = request.POST['id']
        b = Book.objects.filter(id = id).first()
        if b.trang_thai > 0:
            try:
                b.get_content_chapter()
                payload += "Đã cập nhật nội dung chương mới nhất!"
            except:
                payload += "Có lỗi xảy ra!"
        else:
            payload += "Truyện chưa được duyệt"
    else:
        payload += "Sai phương thức nhập!"
    return HttpResponse(payload)

