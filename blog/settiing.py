from tornado.options import define, options
import os
import logging
import tornado
import tornado.template
import motor.motor_tornado
import hashlib


ROOT = os.path.dirname(__file__)    #根路径
create_path = lambda root, *a: os.path.join(root, *a)

TEMPLATES_ROOT = create_path(ROOT, 'templates')
MEDIA_ROOT = create_path(ROOT, 'static')

mongo_client = motor.motor_tornado.MotorClient("127.0.0.1", 27017)

#ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

#development setting
settings = {
    'debug': True,
    'template_loader': tornado.template.Loader(TEMPLATES_ROOT),
    'static_path': MEDIA_ROOT,
    'mongo_client': mongo_client
}

#produce setting




#md5加密
def encrypt_pwd(pwd_str):
    m = hashlib.md5()
    b = pwd_str.encode(encoding='utf-8')
    m.update(b)
    pwd_md5 = m.hexdigest()
    return pwd_md5