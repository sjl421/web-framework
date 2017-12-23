from models import Model
import hashlib


class User(Model):
    """
    保存用户数据的 model
    """
    username: str
    password: str

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = password + salt
        hash = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return hash

    @classmethod
    def register(cls, form):
        """
        注册用户
        """
        username = form['username']
        password = form['password']
        u = User.find_by(username=username)
        if u is None:
            form['password'] = cls.salted_password(password)
            cls.new(form)
            return True
        else:
            return False

    @classmethod
    def validate_login(cls, form):
        """
        验证登录
        """
        username = form['username']
        password = form['password']
        u = cls.find_by(username=username)
        print('uuuu,',u)
        if u is not None:
            print('aaa',u.password == cls.salted_password(password))
            return u.password == cls.salted_password(password)
        else:
            return False
