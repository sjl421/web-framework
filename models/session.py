from models import Model


class Session(Model):
    """
    保存 session 的 model
    """
    session_id: str
    user_id: int
