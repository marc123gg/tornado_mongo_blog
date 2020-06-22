import tornado
import tornado.web
from tornado import gen
from time import ctime
import platform
from datetime import datetime

login_log_local = []
login_name_local = ''

class Admin_Login(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/login.html')



class Admin_Index(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        username = self.get_argument('name')
        password = self.get_argument('pwdPrompt')
        mongo_client = self.settings['mongo_client']
        mongo_db = mongo_client.Myblog
        UserInf = yield mongo_db.admin.find_one({'username': username})
        if UserInf:
            if password == UserInf['password']:
                admin_count = yield mongo_db.admin.count_documents({})
                yield mongo_db.admin.update_one({'username': username},
                                                {"$set": {'login_num': UserInf['login_num'] + 1,'ip':self.request.remote_ip,'login_time':ctime()}})
                yield mongo_db.adminlog.insert_one({'ip': self.request.remote_ip,'time': ctime(), 'status':'成功'})
                login_log = []
                cursor =  mongo_db.adminlog.find({}).sort('time')
                for item in (yield cursor.to_list(length=100)):
                    login_log.append(item)

                login_log_local = login_log
                login_name_local = username

                system_inf = {
                    'login_system':platform.platform(),
                    'login_ip':self.request.remote_ip,
                    'server_inf': 'ubuntu-server-19.04-i686-with-2020.01.04',
                    'admin_count': admin_count,
                    'python_vision':'3.7.0',
                    'python_exp':'cpython',
                    'Mongo_version':'2.6',
                    'now_time': ctime(),
                    'soft_code': 'UTF-8',
                    'soft_version': 'Myblog 1.0'
                }

                self.render('admin/index.html',login_log=login_log,system_inf=system_inf,admin_name=username,login_num=int(UserInf['login_num']+1), prev_ip=UserInf['ip'],prev_time = UserInf['login_time'])
            else:
                yield mongo_db.adminlog.insert_one({'ip': self.request.remote_ip, 'time': ctime(), 'status': '密码错误'})
                self.write('密码错误!')

        else:
            yield mongo_db.adminlog.insert_one({'ip': self.request.remote_ip, 'time': ctime(), 'status': '账号不存在'})
            self.write('密码不存在!')



class Manage_Notify(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/notice.html')

class Add_Notify(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/add-notice.html',login_log=login_log_local)

    @gen.coroutine
    def post(self):

        if self.get_argument('content') == '' or self.get_argument('title') == '' :
            self.write('不能为空')
            self.finish()

        mongo_client = self.settings['mongo_client']
        mongo_db = mongo_client.Myblog

        new_notify = {
            'notify_title': self.get_argument('title'),
            'notify_ispublic': self.get_argument('visibility'),
            'notify_describe': self.get_argument('describe'),
            'notify_content' : self .get_argument('content'),
            'notify_time': self.get_argument('time')
        }
        try:
            yield mongo_db.notify.insert_one(new_notify)
        except:
            self.write('添加成功')
            self.redirect('/admin/add-notify')

class Manage_Comment(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/comment.html')

class Manage_Category(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/category.html')

class Manage_Flink(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/flink.html')