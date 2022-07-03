import re
from book.extensions import trans_for_text, trans_author,get_hostbk
from django import template
from ..models import Book


register = template.Library()

def trans_text(text):
    trans = trans_for_text(text).get_text().title()
    return trans
register.filter("trans_text", trans_text)

def trans_authr(txt):
    trans = trans_author(txt).get_text().title()
    return trans
register.filter("trans_author", trans_authr)

def trans_des(txt):
    trans = trans_for_text(txt).get_text('<br><br>')
    return trans
register.filter("trans_des", trans_des)
    

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
register.filter("check_url", check_url)

def g_host(url):
    host = get_hostbk(url)
register.filter("g_host", g_host)

def get_host_id(url):
    try:
        host_id = url.split("/")[4]
    except:
        host_id = host_id = Book.objects.filter(url = url).first().id
    return host_id
register.filter("get_host_id", get_host_id)

def array_items(id,data):
    return data[id]
register.filter("array_items", array_items)