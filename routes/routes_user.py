from routes import (
    redirect,
    add_session_headers,
    http_response
)
from utils import log
from utils import template
from models.user import User


def route_login(request):
    """
    登录页面的路由函数
    """
    if request.method == 'POST':
        form = request.form()
        if User.validate_login(form):
            user = User.find_by(username=form['username'])
            headers = add_session_headers(user)
            return redirect('/', headers)
    body = template('login.html')
    return http_response(body)


def route_register(request):
    """
    注册页面的路由函数
    """
    if request.method == 'POST':
        form = request.form()
        if User.register(form):
            return redirect('/login')
        else:
            return redirect('/register')
    body = template('register.html')
    return http_response(body)


def route_dict():
    r = {
        '/login': route_login,
        '/register': route_register,
    }
    return r
