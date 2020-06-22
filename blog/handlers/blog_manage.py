import tornado
import tornado.web
from tornado import gen
import random
import json
import base64
import os
import stat
from datetime import datetime
from blog.handlers.admin import login_name_local, login_log_local
from blog.tools import Pagination
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Blog_Index(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        page = self.get_argument('page',1)
        mongo_client = self.settings['mongo_client']
        mongo_db = mongo_client.Myblog
        blog_num = yield mongo_db.blog.count_documents({})
        blog_all = []
        cursor = mongo_db.blog.find({})
        for blog in (yield cursor.to_list(length=50)):
            blog_all.append(blog)
        page_obj = Pagination(blog_num, 10, page)
        blog_show = []
        if page_obj.end > blog_num:
            blog_show = blog_all[page_obj.start:]
        else:
            blow_show = blog_all[page_obj.start, page_obj.end]
        self.render('admin/article.html',blog_show=blog_show, page_html=page_obj.create_html('/admin/blog?page='))

class Blog_add(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        mongo_client = self.settings['mongo_client']
        mongo_db = mongo_client.Myblog
        cursor = mongo_db.blog_classify.find({})
        classifyAll = []
        for classify in (yield cursor.to_list(length=10)):
            classifyAll.append(classify)
        self.render('admin/add-article.html',classifyAll=classifyAll)

    @gen.coroutine
    def post(self):
        if self.get_argument('content') == '' or self.get_argument('titlepic') == '' or self.get_argument('title') == '':
            self.write('不能为空')
            self.finish()

        new_blog = {
        'blog_title' : self.get_argument('title'),
        'blog_content':self.get_argument('content'),
        'blog_Ispublish' : self.get_argument('visibility'),
        'blog_classify' : self.get_argument('category'),
        'blog_tags' : self.get_argument('tags'),
        'blog_titlepic' : self.get_argument('titlepic'),
        'blog_time' : self.get_argument('time'),
        'blog_describe':self.get_argument('describe'),
        'blog_comments': [],
        'blog_readnum': 0
        }

        mongo_client = self.settings['mongo_client']
        mongo_db = mongo_client.Myblog
        try:
            yield mongo_db.blog.insert_one(new_blog)
        except:
            self.write('增加失败')
            self.finish()
        else:
            self.write("增加成功，内容为{}".format(self.get_argument('content')))
            self.finish()

class Blog_Update(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        mongo_client = self.settings['mongo_client']
        mongo_db = mongo_client.Myblog
        cursor = mongo_db.blog_classify.find({})
        classifyAll = []
        for classify in (yield cursor.to_list(length=10)):
            classifyAll.append(classify)
        update_title = self.get_argument('blog_title')
        blog = yield mongo_db.blog.find_one({'blog_title':update_title})
        self.render('admin/update-article.html',blog=blog,classifyAll=classifyAll)

    @gen.coroutine
    def post(self):
        mongo_client = self.settings['mongo_client']
        mongo_db = mongo_client.Myblog
        update_blog_title = self.get_argument('update_blog_title')
        if self.get_argument('titlepic') == '':
            update_blog = {
                'blog_title': self.get_argument('title'),
                'blog_content': self.get_argument('content'),
                'blog_Ispublish': self.get_argument('visibility'),
                'blog_classify': self.get_argument('category'),
                'blog_tags': self.get_argument('tags'),
                #'blog_titlepic': self.get_argument('titlepic'),
                'blog_time': self.get_argument('update_blog_time'),
                'blog_describe': self.get_argument('describe'),
                'blog_comments': []
            }
        else:
            update_blog = {
                'blog_title': self.get_argument('title'),
                'blog_content': self.get_argument('content'),
                'blog_Ispublish': self.get_argument('visibility'),
                'blog_classify': self.get_argument('category'),
                'blog_tags': self.get_argument('tags'),
                'blog_titlepic': self.get_argument('titlepic'),
                'blog_time': self.get_argument('update_blog_time'),
                'blog_describe': self.get_argument('describe'),
                'blog_comments': []
            }
        yield mongo_db.blog.update_one({'blog_title':update_blog_title},{"$set": update_blog})
        self.write('成功')
        self.redirect('/admin/blog')

class Blog_Delete(tornado.web.RequestHandler):
    def post(self):
        self.get_argument('')

class Upload(object):
    ''' upload image or file    '''
    def __init__(self):
        self.config = {}

        self.oriName = ''      # 原始文件名
        self.fileName = ''     # 新文件名
        self.fullName = ''     # 完整文件名,即从当前配置目录开始的URL
        self.filePath = ''     # 完整文件名,即从当前配置目录开始的URL
        self.fileSize = 0      # 文件大小
        self.fileType = ''     # 文件类型
        self.stateMap = {
            "SUCCESS": "SUCCESS",             # 上传成功标记，在UEditor中内不可改变，否则flash判断会出错
            "ERROR_FILE_MAXSIZE": "文件大小超出 upload_max_filesize 限制",
            "ERROR_FILE_LIMITSIZE": "文件大小超出 MAX_FILE_SIZE 限制",
            "ERROR_FILE_UPLOAD_FAILED": "文件未被完整上传",
            "ERROR_FILE_NOT_UPLOAD": "没有文件被上传",
            "ERROR_FILE_NULL": "上传文件为空",
            "ERROR_SIZE_EXCEED": "文件大小超出网站限制",
            "ERROR_TYPE_NOT_ALLOWED": "文件类型不允许",
            "ERROR_CREATE_DIR": "目录创建失败",
            "ERROR_DIR_NOT_WRITEABLE": "目录没有写权限",
            "ERROR_FILE_SAVE": "文件保存时出错",
            "ERROR_FILE_NOT_FOUND": "找不到上传文件",
            "ERROR_WRITE_CONTENT": "写入文件内容错误"
        }

    def getItem(self, key):
        fp = open("F:\\blogBy_tornado\\blog\\media\\admin\\lib\\ueditor\\config.json", 'r')
        config = json.loads(fp.read())
        fp.close()
        for k, v in config.items():
            if k == key:
                return v

    def getStateInfo(self, stateinfo):
        for k, v in self.stateMap.items():
            if k == stateinfo:
                return v

    def checkSize(self):
        if self.fileSize > self.config['maxSize']:
            return False
        else:
            return True

    def checkType(self):
        if self.fileType in self.config['allowFiles']:
            return True
        else:
            return False

    def getFullName(self):
        now = datetime.now()
        randint = random.randint(100000, 999999)
        format = self.config['pathFormat']
        format = format.replace("{yyyy}", now.strftime("%Y"))
        format = format.replace("{mm}", now.strftime("%m"))
        format = format.replace("{dd}", now.strftime("%d"))
        format = format.replace("{time}", now.strftime("%H%M%S"))
        format = format.replace("{rand:6}", str(randint))

        ext = self.oriName[self.oriName.rfind("."):]
        self.fileName = "%s%s%s" % (now.strftime("%H%M%S"), randint, ext)
        return format + ext

    def getFilePath(self):
        fullpath = os.path.join(basedir, self.fullName)
        return fullpath

    def uploadFile(self, upfile):
        result = {'state': '', 'url': '', 'title': '', 'original': ''}

        if not upfile or len(upfile) == 0:
            result['state'] = self.getStateInfo('ERROR_FILE_NOT_UPLOAD')
            return result

        self.oriName = upfile[0]['filename']
        self.fileType = self.oriName[self.oriName.rfind('.'):]
        data = upfile[0]['body']
        self.fileSize = len(data)

        if self.fileSize == 0:
            result['state'] = self.getStateInfo('ERROR_FILE_NULL')
            return result

        if not self.checkSize():
            result['state'] = self.getStateInfo('ERROR_SIZE_EXCEED')
            return result

        if not self.checkType():
            result['state'] = self.getStateInfo('ERROR_TYPE_NOT_ALLOWED')
            return result

        self.fullName = self.getFullName()
        self.filePath = self.getFilePath()

        dirname = os.path.dirname(self.filePath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except Exception as e:
                result['state'] = self.getStateInfo('ERROR_CREATE_DIR')
                return result

        if not os.access(dirname, os.R_OK | os.W_OK):
            try:
                os.chmod(dirname, stat.S_IREAD | stat.S_IWRITE)
            except Exception as e:
                result['state'] = self.getStateInfo('ERROR_DIR_NOT_WRITEABLE')
                return result

        try:
            fp = open(self.filePath, 'wb')
            fp.write(data)
            fp.close()
        except Exception as e:
            result['state'] = self.getStateInfo('ERROR_FILE_SAVE')
            return result

        result['state'] = self.stateMap['SUCCESS']
        result['url'] = self.fullName
        result['title'] = self.fileName
        result['original'] = self.oriName
        return result

    def getFileList(self, start, size):
        result = {'state': '', 'list': [], 'start': 0, 'total': 0}
        path = self.config['path']
        listSize = self.config['listSize']
        print(listSize)
        listfiles = []
        for root, dirs, files in os.walk(path):
            for file in files:
                self.fileType = file[file.rfind('.'):]
                if self.checkType():
                    url = root + '/' + file
                    listfiles.append({'url': '%s' % url})

        if size > listSize:
            num = listSize
        else:
            num = size

        listfiles.sort()
        lists = listfiles[start:(start + num)]

        result['state'] = self.stateMap['SUCCESS']
        result['list'] = lists
        result['start'] = start
        result['total'] = len(listfiles)
        return result


class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        action = self.get_argument('action')
        upload = Upload()
        result = {}
        if action == "config":
            fp = open("F:\\blogBy_tornado\\blog\\media\\admin\\lib\\ueditor\\config.json", 'r')
            config = json.loads(fp.read())
            fp.close()
            result = config

        if action == "listimage":
            start = self.get_argument('start')
            size = self.get_argument('size')

            upload.config['path'] = upload.getItem('imageManagerListPath')
            upload.config['listSize'] = upload.getItem('imageManagerListSize')
            upload.config['allowFiles'] = upload.getItem('imageManagerAllowFiles')

            result = upload.getFileList(int(start), int(size))

        if action == "listfile":
            start = self.get_argument('start')
            size = self.get_argument('size')

            upload.config['path'] = upload.getItem('fileManagerListPath')
            upload.config['listSize'] = upload.getItem('fileManagerListSize')
            upload.config['allowFiles'] = upload.getItem('fileManagerAllowFiles')

            result = upload.getFileList(int(start), int(size))

        self.write(result)

    def post(self):
        action = self.get_argument('action')
        upload = Upload()
        result = {}

        if action == "uploadimage":
            fieldName = upload.getItem('imageFieldName')
            upload.config['pathFormat'] = upload.getItem('imagePathFormat')
            upload.config['maxSize'] = upload.getItem('imageMaxSize')
            upload.config['allowFiles'] = upload.getItem('imageAllowFiles')

            upfile = self.request.files[fieldName]
            result = upload.uploadFile(upfile)

        if action == "uploadfile":
            fieldName = upload.getItem('fileFieldName')
            upload.config['pathFormat'] = upload.getItem('filePathFormat')
            upload.config['maxSize'] = upload.getItem('fileMaxSize')
            upload.config['allowFiles'] = upload.getItem('fileAllowFiles')

            upfile = self.request.files[fieldName]
            result = upload.uploadFile(upfile)

        if action == "uploadvideo":
            fieldName = upload.getItem('videoFieldName')
            upload.config['pathFormat'] = upload.getItem('videoPathFormat')
            upload.config['maxSize'] = upload.getItem('videoMaxSize')
            upload.config['allowFiles'] = upload.getItem('videoAllowFiles')

            upfile = self.request.files[fieldName]
            result = upload.uploadFile(upfile)

        if action == "uploadscrawl":
            upload.config['pathFormat'] = upload.getItem('scrawlPathFormat')
            upload.config['maxSize'] = upload.getItem('scrawlMaxSize')
            upload.config['allowFiles'] = ['.png']

            data = self.request.body_arguments
            upfile = []
            upfile.append({'filename': 'scrawl.png', 'body': base64.b64decode(data['upfile'][0])})
            result = upload.uploadFile(upfile)

        self.write(result)

