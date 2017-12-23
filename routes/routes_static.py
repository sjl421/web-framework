from routes import login_required, current_user, http_response
from utils import template, log


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    u = current_user(request)
    if u is None:
        username = '游客'
    else:
        username = u.username
    body = template('index.html', username=username)
    return http_response(body)


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def route_dict():
    r = {
        '/': route_index,
        '/static': route_static,
    }
    return r
