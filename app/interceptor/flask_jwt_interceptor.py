from flask_jwt_extended import verify_jwt_in_request

def custom_jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        # 在此处可以添加自定义的校验逻辑
        # 如果校验失败，可以返回错误响应或执行其他操作
        # 如果校验成功，可以继续执行被装饰的函数
        return fn(*args, **kwargs)
    return wrapper

