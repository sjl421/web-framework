from models.session import Session
from utils import log, gmt_time
from models.user import User
import random

session = {}


def random_str():
    """
    生成一个 16 位随机的字符串，用来设置 session
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 1)
        s += seed[random_index]
    return s


def add_session_headers(user=None, expired_month=0):
    """
     为注册或登录成功的 user 响应头加上 session
    """
    session_id = random_str()
    if user is None:
        user_id = session_id
    else:
        user_id = user.id
    s = Session.new(dict(
        session_id=session_id,
        user_id=user_id,
    ))
    s.save()
    expired_time = gmt_time(expired_month)
    headers = {
        'Set-Cookie': 'sid={}; Expires={}; path=/'.format(session_id, expired_time),
    }
    return headers


def current_user(request):
    """
    根据 session_id 找到当前请求对应的 user 实例
    """
    session_id = request.cookies.get('sid', '')
    log(request.cookies)
    log('sssssss',session_id)
    sessions = Session.all()
    log('sesese', sessions)
    for s in sessions:
        if s.session_id == session_id:
            log('yyyyyy')
            u = User.find_by(id=s.user_id)
            log('s.userid',s.user_id)
            log('u',u)
            return u
    return None


def response_with_headers(headers=None, status_code=200):
    """
    生成响应头，例子如下所示：
    Content-Type: text/html
    Set-Cookie: user=zch
    """
    header = 'HTTP/1.1 {} OK\r\nContent-Type: text/html\r\n'
    header = header.format(status_code)
    if headers is not None:
        header += ''.join([
            '{}: {}\r\n'.format(k, v) for k, v in headers.items()
        ])
    return header


def redirect(location, headers=None):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    h = {
        'Location': location
    }
    if headers is not None:
        h.update(headers)
    header = response_with_headers(h, 302)
    r = header + '\r\n' + ''
    return r.encode()


def login_required(route_function):
    """
    登录验证函数
    """

    def f(request):
        u = current_user(request)
        if u is None:
            return redirect('/login')
        else:
            return route_function(request)

    return f


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def http_response(body, headers=None):
    """
    headers 是可选的字典格式的 HTTP 头部
    """
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()
