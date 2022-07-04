import re, requests
from bs4 import BeautifulSoup

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def check_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    check = re.match(regex, url) is not None # True
    return check

def request_url(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36"
    }
    try:
        r = requests.get(url=url,headers=headers)
        r.encoding='utf-8-sig'
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup
    except:
        return 0

def trans_for_text(txt):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36"
    }
    data = {
        "chineseContent": txt
    }
    try:
        r = requests.post(url='https://vietphrase.info/Vietphrase/TranslateVietPhraseS',headers=headers,data=data)
        r.encoding='utf-8-sig'
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup
    except:
        return 0
    
def trans_author(txt):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36"
    }
    data = {
        "chineseContent": txt
    }
    try:
        r = requests.post(url='https://vietphrase.info/Vietphrase/TranslateHanViet',headers=headers,data=data)
        r.encoding='utf-8-sig'
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup
    except:
        return 0

def get_hostbk(url):
    if re.findall("uuxs",url):
        host = "uuxs"
    else:
        host = url
    return host

def about_bk(url):
    host = get_hostbk(url)
    context = {}
    host_list = [ "uuxs" ]
    if host in host_list:
        soup = request_url(url)
        if host == "uuxs":
            title = soup.select_one('#__layout > div > div:nth-child(2) > div.frame_body > div.pure-g.novel_info > div.pure-u-xl-5-6.pure-u-lg-5-6.pure-u-md-2-3.pure-u-1-2 > ul > li:nth-child(1) > h1').get_text().replace(' ','')
            author = soup.select_one('#__layout > div > div:nth-child(2) > div.frame_body > div.pure-g.novel_info > div.pure-u-xl-5-6.pure-u-lg-5-6.pure-u-md-2-3.pure-u-1-2 > ul > li:nth-child(2) > a').get_text().replace(' ','')
            des = soup.select_one('#__layout > div > div:nth-child(2) > div.frame_body > div.description > div').get_text('<br>').replace(' ','')
            context['title'] = title
            context['author'] = author
            context['des'] = des
            return context
        return False
    return False