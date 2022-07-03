import json
from multiprocessing import context
from .models import Book, Rating
from .extensions import check_url, trans_for_text, trans_author, request_url
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
            host = key.split(".")[1]
            appect_host = ['uuxs','writter','convert']
            if not host in appect_host:
                messages.error(request, 'Nguồn này web chưa hỗ trợ nhé.')
                return redirect("home")
            check = Book.objects.filter(url = key).first()
            if check:
                return redirect('book_home',host= key.split(".")[1], host_id=key.split("/")[4])
            if host == "uuxs":
                soup = request_url(key)
                title = soup.select_one('#__layout > div > div:nth-child(2) > div.frame_body > div.pure-g.novel_info > div.pure-u-xl-5-6.pure-u-lg-5-6.pure-u-md-2-3.pure-u-1-2 > ul > li:nth-child(1) > h1').get_text()
                author =soup.select_one('#__layout > div > div:nth-child(2) > div.frame_body > div.pure-g.novel_info > div.pure-u-xl-5-6.pure-u-lg-5-6.pure-u-md-2-3.pure-u-1-2 > ul > li:nth-child(2) > a').get_text()
                des = soup.select_one('#__layout > div > div:nth-child(2) > div.frame_body > div.description > div').get_text('<br>')
            b = Book.objects.create(title= title, author=author, des = des, user=request.user,url=key)
            b.save()
            return redirect('book_home',host= key.split(".")[1], host_id=key.split("/")[4])
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
    try:
        bk = Book.objects.filter(id=bk_id).first()
        f = open(bk.chapter.path, encoding='utf-8')
        data = json.load(f)
        length = len(data)
        context['url'] = bk.url
    except:
        data = []
        length = 0
    context['data'] = zip(range(length),data)
    return render(request, 'book/chapter_list.html', context)

def data_chap(request,host,host_id,chap_id):
    return 0

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