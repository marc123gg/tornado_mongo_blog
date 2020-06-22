import tornado.ioloop
import tornado.web
from blog.handlers.base import BlogIndex,Article,About_Me
from blog.handlers.admin import Admin_Login,Admin_Index, Manage_Notify,Manage_Category,Manage_Comment,Manage_Flink,\
    Add_Notify
from blog.handlers.blog_manage import Blog_Index, Blog_add, UploadHandler, Blog_Update
from blog.settiing import settings
from tornado.web import url

def make_app():
    return tornado.web.Application([
        url(r"/", BlogIndex, name='blog_main'),
        url(r"/aboutMe", About_Me, name='blog_aboutme'),
        url(r"/article/total", Article, name='blog_details'),
        url(r"/admin", Admin_Login, name='admin_login'),
        url(r"/admin/index", Admin_Index, name='admin_index'),
        url(r"/admin/blog", Blog_Index, name="blog_index"),
        url(r"/admin/blog/add", Blog_add, name="blog_add"),
        url(r"/admin/blog/update", Blog_Update, name="blog_update"),
        url(r"/admin/manage-notify", Manage_Notify, name="manage_notify"),
        url(r"/admin/add-notify", Add_Notify, name="add_notify"),
        url(r"/admin/manage-flin", Manage_Flink, name="manage_flink"),
        url(r"/admin/manage-comment", Manage_Comment, name="manage_comment"),
        url(r"/admin/manage-category", Manage_Category, name="manage_category"),
        url(r"/upload", UploadHandler , name='upload_riceText')
    ], **settings)

def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()