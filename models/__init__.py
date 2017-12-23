import json
import time
from utils import log


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


class Model(object):
    """
    所有 model 的基类
    """

    def __init__(self, form):
        """
        使用 annotation 可以在基类里实现 update，
        但只有 py3.5 以上版本可以使用
        """
        annotations = {}
        annotations.update(self.__annotations__)
        # annotations.update(Model.__annotations__)
        for name, t in annotations.items():
            if name in form:
                value = form[name]
                value = t(value)
                setattr(self, name, value)
            else:
                setattr(self, name, t())

    @classmethod
    def new(cls, form):
        """
        初始化一个 cls，单独设置此函数可以实现功能扩充：保存，log等
        """
        m = cls(form)
        m.save()
        return m

    @classmethod
    def db_path(cls):
        """
        返回文件的路径，文件名与 cls 的名字相同
        """
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def _new_from_dict(cls, d):
        """
        根据 txt 文件里的数据初始化一个 cls 实例
        """
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v)
        return m

    @classmethod
    def all(cls):
        """
        返回所有的实例
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        根据指定条件，返回一个符合的 cls 实例
        """
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k, None):
                    exist = True
                else:
                    exist = False
            if exist:
                return m
        return None

    @classmethod
    def find(cls, id):
        """
        根据 id 查找 cls 实例
        """
        return cls.find_by(id=id)

    @classmethod
    def find_all(cls, **kwargs):
        """
        根据指定条件，返回所有符合的 cls 实例
        """
        models = []
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k, None):
                    exist = True
                else:
                    exist = False
                    break
            if exist:
                models.append(m)
        return models

    def __repr__(self):
        """
        设置打印字符串格式为：
        < Model
        id: (10)
        session_id: (gg4j2g2jdej24252)
        >
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        """
        把 cls 实例保存到 txt 文件中
        """
        models = self.all()
        log('models', models)
        first_index = 0
        # 新 cls 没有 id，自动为 cls 添加 id 并将 cls 加入 models 中
        if getattr(self, 'id', None) is None:
            if len(models) > 0:
                self.id = models[-1].id + 1
            else:
                self.id = first_index
            models.append(self)

        # cls 更新时，根据已有 id 完成新旧 cls 的替换
        else:
            log('self',self)
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        # 保存
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    @classmethod
    def update(cls, id, form):
        """
        根据 id 和 form 更新指定的 cls 实例
        """
        t = cls.find(id)
        for key in form:
            # 只更新设定的内容
            if key in cls.__annotations__:
                # 强制转化更新内容的类型
                t = cls.__annotations__[key]
                setattr(t, key, t(form[key]))
        t.updated_time = int(time.time())
        t.save()

    @classmethod
    def delete(cls, id):
        """
        根据 id 删除指定的 cls 实例
        """
        ms = cls.all()
        for i, m in enumerate(ms):
            if m.id == id:
                del ms[i]
                break
        # 保存
        l = [m.__dict__ for m in ms]
        path = cls.db_path()
        save(l, path)
