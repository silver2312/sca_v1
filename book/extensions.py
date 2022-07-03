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
    if url.find("uuxs") > 0:
        host = "uuxs"
    else:
        host = url
    return host