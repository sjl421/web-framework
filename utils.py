import time
from jinja2 import Environment, FileSystemLoader


def log(*args, **kwargs):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, **kwargs)
        print(dt, *args, file=f, **kwargs)


# 用于加载模板的目录
path = 'templates'
# 创建一个加载器, jinja2 会从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境, 有了它才能读取模板文件
env = Environment(loader=loader)


def template(path, **kwargs):
    """
    读取路径里的模板并渲染返回
    """
    t = env.get_template(path)
    return t.render(**kwargs)


def formatted_time(unixtime):
    dt = time.localtime(unixtime)
    ds = time.strftime('%Y-%m-%d %H:%M:%S', dt)
    return ds


def gmt_time(month=0):
    format = '%a, %d %b %Y %H:%M:%S GMT'
    second = month * 30 * 24 * 60 * 60
    value = time.localtime(int(time.time()) + second)
    dt = time.strftime(format, value)
    return dt