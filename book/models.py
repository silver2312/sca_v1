import os, requests, json
import re
from re import sub
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import Users
from .extensions import request_url, trans_for_text,get_hostbk
from PIL import Image
# Create your models here.

class TheLoai(models.Model):
    name = models.CharField(max_length=100)
    des = models.TextField()
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    des = models.TextField()
    def __str__(self):
        return self.name
    
def chapter_path(self):
    chapter = 'static/upload/book/{0}/chapter.json'.format(self.id)
    return chapter
def cmt_path(self):
    cmt = 'static/upload/book/{0}/cmt.json'.format(self.id)
    return cmt
def name_path(self,filename):
    name = 'static/upload/book/{0}/name.txt'.format(self.id)
    return name
def image_book_path(self,filename):
    image = 'static/upload/book/{0}/image.png'.format(self.id)
    if os.path.exists(image):
        os.remove(image)
    return image

class Book(models.Model):
    TRANG_THAI_CHOISE = (
        (0, 'Chưa duyệt'),
        (1, 'Còn tiếp'),
        (2, 'Tạm dừng'),
        (3,'Đã xong'),
    )
    title = models.CharField(max_length=100, verbose_name='Tên truyện')
    image = models.ImageField(max_length=255,null = True,blank = True,upload_to = image_book_path, default='static/img/brand/image_book.png',verbose_name='Ảnh truyện')
    author = models.CharField(max_length=100,verbose_name='Tác giả')
    url = models.TextField(null=True, blank=True)
    des = models.TextField(null = True,blank=True, verbose_name='Mô tả truyện đầy đủ')
    user = models.ForeignKey(Users, on_delete=models.SET_NULL,null=True ,blank=True , verbose_name='Người đăng')
    the_loai = models.ManyToManyField(TheLoai, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)
    trang_thai = models.IntegerField(choices=TRANG_THAI_CHOISE,default=0,verbose_name="Trạng thái")
    gift = models.FloatField(default=0)
    de_cu = models.BooleanField(default=False, verbose_name='Đề cử')
    date_add = models.DateTimeField(auto_now_add=True, verbose_name='Ngày đăng')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    chapter = models.FileField(max_length=255, null=True, blank=True, upload_to=chapter_path,verbose_name='Danh sách chương')
    comment = models.FileField(max_length=255, null=True, blank=True, upload_to=cmt_path ,verbose_name='Bình luận')
    name_bk = models.FileField(max_length=255, null=True, blank=True, upload_to=name_path,verbose_name='Gói name')
    def __str__(self):
        return self.title
    def check_file(self):
        #check file
        check = 0
        name = 'static/upload/book/{0}/{1}'.format(self.id, 'name.txt')
        if os.path.exists(name) == False:
            os.makedirs(os.path.dirname(name), exist_ok=True)
            f = open(name, 'w')
            self.name_bk = name
            check = 1
        else:
            if self.name_bk != name:
                self.name_bk = name
                check = 1
        cmt = 'static/upload/book/{0}/{1}'.format(self.id, 'cmt.json')
        if os.path.exists(cmt) == False:
            os.makedirs(os.path.dirname(cmt), exist_ok=True)
            f = open(cmt, 'w')
            self.comment = cmt
            check = 1
        else:
            if self.comment != cmt:
                self.comment = cmt
                check = 1
        chapter = 'static/upload/book/{0}/{1}'.format(self.id, 'chapter.json')
        if os.path.exists(chapter) == False:
            os.makedirs(os.path.dirname(chapter), exist_ok=True)
            f = open(chapter, 'w')
            self.chapter = chapter
            check = 1
        else:
            if self.chapter != chapter:
                self.chapter = chapter
                check = 1
        if check == 1:
            self.save()
    def download_image(self):
        if  self.image == "static/img/brand/image_book.png":
            soup = request_url(self.url)
            if self.url.split(".")[1] == "uuxs":
                image_url = soup.select_one('#__layout > div > div:nth-child(2) > div.frame_body > div.pure-g.novel_info > div.pure-u-xl-1-6.pure-u-lg-1-6.pure-u-md-1-3.pure-u-1-2 > a > amp-img').attrs['src']
                image = 'static/upload/book/{0}/image.png'.format(self.id)
                img = Image.open(requests.get("https://www.uuxs.com"+image_url, stream = True).raw)
                img.save(image)
                self.image = image
                self.save()
    def get_chaplist(self):
        host = get_hostbk(self.url)
        host_list = [ "uuxs" ]
        if host in host_list:
            id = self.url.split("/")[4]
            if self.chapter:
                url = 'https://www.uuxs.com/catalog/'+id
                soup = request_url(url)
                list_chap = soup.select('#__layout > div > div:nth-child(2) > div.frame_body > div.chapters_frame > div > div > a')
                try:
                    f = open(self.chapter.path ,encoding='utf-8')
                    data = json.load(f)
                    lenght = len(data)
                except:
                    lenght = 0
                    data = []
                for val in list_chap:
                    txt = val.get_text()
                    arr = list(txt)
                    a = 0
                    for i in range(len(arr)):
                        if arr[i] == "章":
                            a = i+1
                            break
                        if arr[i] == " ":
                            a = i+1
                            break
                    sl = arr[a:]
                    title= ""
                    for s in sl:
                        title+=s
                    sub_title = None
                    url = val.attrs['href']
                    content = None
                    if lenght == 0:
                        data.append( { 'title':title, 'url':url, 'sub_title':sub_title,'content':content } )
                    else:
                        check = 0
                        for d in data:
                            if d['url'] == url:
                                check = 1
                        if check == 0:
                            data.append( { 'title':title, 'url':url, 'sub_title':sub_title,'content':content } )
                if len(list_chap) > self.chapter.size:
                    with open(self.chapter.path, 'w', encoding='utf8') as s:
                        json.dump(data,s, indent=4, sort_keys=True, ensure_ascii=False)
                    self.save()
            else:
                return False
        else:
            return False
    def get_sub_title(self):
        if self.chapter :
            try:
                f = open(self.chapter.path ,encoding='utf-8')
                data = json.load(f)
                lenght = len(data)
                for x in range(lenght):
                    if data[x]["sub_title"] is None:
                        data[x]["sub_title"] = trans_for_text(data[x]["title"]).get_text()
                        with open(self.chapter.path, 'w', encoding='utf8') as s:
                            json.dump(data,s, indent=4, sort_keys=True, ensure_ascii=False)
            except:
                return False
    def get_content_chapter(self):
        host_list = [ "uuxs" ]
        host = get_hostbk(self.url)
        if self.chapter and host in host_list:
            try:
                f = open(self.chapter.path ,encoding='utf-8')
                data = json.load(f)
                lenght = len(data)
                for x in range(lenght):
                    if data[x]["content"] is None:
                        if host == "uuxs":
                            soup = request_url('https://www.uuxs.com'+data[x]['url'])
                            data[x]["content"] = soup.select_one('#__layout > div > div:nth-child(2) > div.frame_body > div.content').get_text('<br><br>').replace("&nbsp;", "")
                        with open(self.chapter.path, 'w', encoding='utf8') as s:
                            json.dump(data,s, indent=4, sort_keys=True, ensure_ascii=False)
            except:
                return False
    def get_content_id(self,id_chap):
        host_list = [ "uuxs" ]
        host = get_hostbk(self.url)
        context = {}
        if self.chapter and host in host_list:
            try:
                f = open(self.chapter.path ,encoding='utf-8')
                data = json.load(f)
                lenght = len(data)
                if id_chap > lenght:
                    return False
                if data[id_chap]["content"] is None:
                    if host == "uuxs":
                        soup = request_url('https://www.uuxs.com'+data[id_chap]['url'])
                        data[id_chap]["content"] = soup.select_one('#__layout > div > div:nth-child(2) > div.frame_body > div.content').get_text('<br><br>').replace("&nbsp;", "")
                    with open(self.chapter.path, 'w', encoding='utf8') as s:
                        json.dump(data,s, indent=4, sort_keys=True, ensure_ascii=False)
                context['content'] = data[id_chap]["content"]
                context['sub_title'] = data[id_chap]['title']
                return context
            except:
                return False
    
class GiftList(models.Model):
    book = models.IntegerField(verbose_name="Truyện")
    user = models.IntegerField(verbose_name="Người tặng")
    gift_number = models.FloatField(default=0,validators=[MinValueValidator(1)],verbose_name="Số quà tặng")
    date_add = models.DateTimeField(auto_now=True, verbose_name="Ngày tặng")
    def __str__(self):
        return trans_for_text(self.book.title).get_text()
    
class Rating(models.Model):
    book = models.IntegerField(verbose_name="Truyện")
    user = models.IntegerField(verbose_name="Người đánh giá")
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)],verbose_name="Đánh giá")
    date_add = models.DateTimeField(auto_now=True,verbose_name="Ngày thêm")
    
    def tong(bk):
        try:
            ratings = Rating.objects.filter(book=bk)
            num = 0 
            dem = 0
            for r in ratings:
                num += r.rating
                dem +=1
            return int( num/dem )
        except:
            return 0