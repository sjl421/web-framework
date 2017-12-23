from routes import (
    current_user,
    http_response,
)
from utils import log
from utils import template


def index_(request):
    """
    主页的处理函数, 返回主页的响应
    """
    u = current_user(request)
    log('uuu',u)
    if u is None:
        username = '游客'
    else:
        username = u.username
    body = template('index.html', username=username)
    return http_response(body)