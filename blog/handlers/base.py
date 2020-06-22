import tornado.ioloop
import tornado.web
import os
from blog.tools import Pagination_Show
from tornado import gen

class BlogIndex(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        page = self.get_argument('page', 1)
        mongo_client = self.settings['mongo_client']
        mongo_db = mongo_client.Myblog
        blog_num = yield mongo_db.blog.count_documents({})
        blog_all = []
        cursor = mongo_db.blog.find({})
        for blog in (yield cursor.to_list(length=50)):
            blog_all.append(blog)
        page_obj = Pagination_Show(blog_num, 6, page)
        blog_show = []
        if page_obj.end > blog_num:
            blog_show = blog_all[page_obj.start:]
        else:
            blow_show = blog_all[page_obj.start, page_obj.end]

        self.render('index.html', blog_show=blog_show, page_html=page_obj.create_html('/?page='))

class Article(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        mongo_client = self.settings['mongo_client']
        mongo_db = mongo_client.Myblog
        blog_all = []
        cursor = mongo_db.blog.find({})
        for blog in (yield cursor.to_list(length=50)):
            blog_all.append(blog)
        if len(blog_all) == 0:
            self.write('暂无文章')
            self.finish()
        blog_index = int(self.get_argument('index', 0))
        blog = self.get_argument('title',blog_all[blog_index]['blog_title'])
        current_blog = yield mongo_db.blog.find_one({'blog_title': blog})
        yield mongo_db.blog.update_one({'blog_title': blog},{"$set": {'blog_readnum': current_blog['blog_readnum']+1}})
        html_list = []
        if blog_index == 0:
            html_list.append(
                '<a class="nav-link-prev nav-item d-none nav-link rounded-left" href="#">Previous<i class="arrow-prev fas fa-long-arrow-alt-left"></i></a>')
            if blog_index+1 < len(blog_all):
                html_list.append('<a class="nav-link-next nav-item nav-link rounded-right" href="%s%s">Next<i class="arrow-next fas fa-long-arrow-alt-right"></i></a>' % ('/article/total','?index='+str(blog_index+1)+'&title='+blog_all[blog_index+1]['blog_title']))
            else:
                html_list.append(
                    '<a class="nav-link-next nav-item d-none nav-link rounded-right" href="#">Next<i class="arrow-next fas fa-long-arrow-alt-right"></i></a>')
        else:
            html_list.append('<a class="nav-link-prev nav-item nav-link rounded-left" href="%s%s">Previous<i class="arrow-prev fas fa-long-arrow-alt-left"></i></a>' % ('/article/total','?index='+str(blog_index-1)+'&title='+blog_all[blog_index-1]['blog_title']))
            if blog_index+1 < len(blog_all):
                html_list.append('<a class="nav-link-next nav-item nav-link rounded-right" href="%s%s">Next<i class="arrow-next fas fa-long-arrow-alt-right"></i></a>' % ('/article/total','?index='+str(blog_index+1)+'&title='+blog_all[blog_index+1]['blog_title']))
            else:
                html_list.append(
                    '<a class="nav-link-next nav-item d-none nav-link rounded-right" href="#">Next<i class="arrow-next fas fa-long-arrow-alt-right"></i></a>')

        self.render('blog-post.html',html_list=html_list,current_blog=current_blog)

class About_Me(tornado.web.RequestHandler):
    def get(self):
        self.render('about.html')



ROOT = os.path.abspath(os.path.join(os.getcwd(), ".."))

print(os.path.join(ROOT, 'templates'))