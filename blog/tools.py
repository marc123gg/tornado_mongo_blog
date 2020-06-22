class Pagination(object):
    def __init__(self, total_item, page_item , current_page):
        self.page_num = total_item // page_item + 1
        try:
            self.current_page = int(current_page)
        except:
            self.current_page = 1

        if self.current_page <= 1:
            self.current_page = 1
        if self.current_page >= self.page_num:
            self.current_page = self.page_num

        self.total_item = total_item
        self.page_item = page_item


    @property
    def start(self):
        return (self.current_page-1) * self.page_item

    @property
    def end(self):
        return self.current_page * self.page_item

    def create_html(self,baseurl):
        html_list = []
        if self.current_page == 1:
            html_list.append('<li class="disabled"><a aria-label="Previous"> <span aria-hidden="true">&laquo;</span> </a> </li>')
            html_list.append('<li class="active"><a href="#">1</a></li>')
            if 2 < self.page_num+1:
                for i in range(2,self.page_num+1):
                    html_list.append('<li><a href="%s%s">%s</a></li>' % (baseurl,i,i))
                html_list.append('<li><a href="%s%s" aria-label="Next"> <span aria-hidden="true">&raquo;</span> </a> </li>' % (baseurl, self.current_page+1))
            else:
                html_list.append(
                    '<li class="disabled"><a aria-label="Next"> <span aria-hidden="true">&raquo;</span> </a> </li>')

        else:
            html_list.append('<li><a href="%s%s" aria-label="Previous"> <span aria-hidden="true">&laquo;</span> </a> </li>' % (baseurl,self.current_page-1))
            for i in range(1,self.current_page):
                html_list.append('<li><a href="%s%s">%s</a></li>' % (baseurl, i, i))
            html_list.append('<li class="active"><a href="#">%s</a></li>' % (self.current_page))
            if self.current_page+1 < self.page_num+1:
                for i in  range(self.current_page+1,self.page_num+1):
                    html_list.append('<li><a href="%s%s">%s</a></li>' % (baseurl, i, i))
                html_list.append('<li><a href="%s%s" aria-label="Next"> <span aria-hidden="true">&raquo;</span> </a> </li>' % (baseurl, self.current_page+1))
            else:
                html_list.append('<li class="disabled"><a aria-label="Next"> <span aria-hidden="true">&raquo;</span> </a> </li>')

        return html_list

class Pagination_Show(object):
    def __init__(self, total_item, page_item , current_page):
        self.page_num = total_item // page_item + 1
        try:
            self.current_page = int(current_page)
        except:
            self.current_page = 1

        if self.current_page <= 1:
            self.current_page = 1
        if self.current_page >= self.page_num:
            self.current_page = self.page_num

        self.total_item = total_item
        self.page_item = page_item


    @property
    def start(self):
        return (self.current_page-1) * self.page_item

    @property
    def end(self):
        return self.current_page * self.page_item

    def create_html(self,baseurl):
        html_list = []
        if self.current_page == 1:
            html_list.append('<a class="nav-link-prev nav-item nav-link d-none rounded-left" href="#">Previous<i class="arrow-prev fas fa-long-arrow-alt-left"></i></a>')
            if 2 < self.page_num+1:
                html_list.append('<a class="nav-link-next nav-item nav-link  rounded" href="%s%s">Next<i class="arrow-next fas fa-long-arrow-alt-right"></i></a>')
            else:
                html_list.append(
                    '<a class="nav-link-next nav-item nav-link d-none rounded" href="blog-list.html">Next<i class="arrow-next fas fa-long-arrow-alt-right"></i></a>')

        else:
            html_list.append('<a class="nav-link-prev nav-item nav-link rounded-left" href="%s%s">Previous<i class="arrow-prev fas fa-long-arrow-alt-left"></i></a>' % (baseurl,self.current_page-1))
            if self.current_page+1 < self.page_num+1:
                html_list.append('<a class="nav-link-next nav-item nav-link rounded" href="%s%s">Next<i class="arrow-next fas fa-long-arrow-alt-right"></i></a>' % (baseurl, self.current_page+1))
            else:
                html_list.append('<a class="nav-link-next nav-item nav-link d-none rounded" href="blog-list.html">Next<i class="arrow-next fas fa-long-arrow-alt-right"></i></a>')

        return html_list