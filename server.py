import socket
import _thread
from request import Request
from utils import log
from routes import error
from routes.routes_user import route_dict as user_routes
from routes.routes_static import route_dict as static_routes


def response_for_path(request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {}
    # 注册外部的路由
    r.update(user_routes())
    r.update(static_routes())
    response = r.get(request.path, error)
    return response(request)


def process_request(connection):
    r = connection.recv(1024)
    r = r.decode()
    log('request log:\n{}'.format(r))
    # 把原始请求数据传给 Request 对象
    request = Request(r)
    # 用 response_for_path 函数来得到 path 对应的响应内容
    response = response_for_path(request)
    log("response log:\n{}".format(response.decode()))
    # 把响应发送给客户端
    connection.sendall(response)
    # 处理完请求, 关闭连接
    connection.close()


def run(host, port):
    """
    启动服务器
    """
    log('开始运行于', '{}:{}'.format(host, port))
    with socket.socket() as s:
        # 保证程序重启后使用原有端口
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        while True:
            connection, address = s.accept()
            log('ip {}'.format(address))
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    config = dict(
        host='127.0.0.1',
        port=3000,
    )
    run(**config)