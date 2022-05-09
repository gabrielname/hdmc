import imp
from django.utils.safestring import mark_safe
from math import ceil
import copy

"""自定义分页组件"""
"""
使用方法:
后端:
def prettynum_list(request):
    data_dict = {}
    search_data = request.GET.get('q','')
    if search_data:
        data_dict["mobile__contains"] = search_data
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    
    page_obj = Pagination(request=request,queryset=queryset,
                page_param="page",page_size=10,step=5)  #实例化
    page_queryset = page_obj.page_queryset  #返回当前页面需要显示的数据
    page_string = page_obj.html()       #返回生成的分页组件html标签

    context = {         #传递到前端
        "queryset":page_queryset,
        "search_data":search_data,
        "page_string":page_string,
        }
    
    return render(request,"prettynum_list.html",context)

前端:
    <nav aria-label="Page navigation">
        <ul class="pagination">
            {{page_string}}
        </ul>
    </nav>
"""

class Pagination(object):
    
    def __init__(self,request,queryset,page_param = "page",page_size = 10,step = 5):
        """
        Params:
            request: request请求
            queryset: 数据库获取的所有数据
            page_param: url传递的参数中页码所在的字段名
            page_size: 页面包含的数据条数
            step: 要显示的当前页面的前后相邻页数
        """
        self.page_param = page_param
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.query_dict.setlist(self.page_param,[1])
        page = request.GET.get(self.page_param,"1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        
        self.page = page
        self.page_size = page_size

        self.start = (page -1) * page_size
        self.end = page * page_size

        self.queryset = queryset
        self.page_queryset = queryset[self.start:self.end]
        self.step = step
        self.num = len(self.queryset)
        self.page_num = ceil(self.num / page_size)
        if self.page_num <= 2* step + 1:
            self.start_page = 1
            self.end_page = self.page_num
        else:
            if page <= step:
                self.start_page = 1
                self.end_page = 2 * step + 1
        
            else:
                if page + step > self.page_num:
                    self.start_page = page - step
                    self.end_page = self.page_num
                else:
                    self.start_page = page - step
                    self.end_page = page + step

    def html(self):
        page_str_list = []

        self.query_dict.setlist(self.page_param,[1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        if self.page > 1:
            self.query_dict.setlist(self.page_param,[self.page - 1])
            prev = '<li><a href="?{}"><<</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param,[1])
            prev = '<li><a href="?{}"><<</a></li>'.format(self.query_dict.urlencode())   
        page_str_list.append(prev)

        for i in range(self.start_page,self.end_page + 1):
            self.query_dict.setlist(self.page_param,[i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(),i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(),i)
            page_str_list.append(ele)
        
        if self.page == self.page_num:
            self.query_dict.setlist(self.page_param,[self.page_num])
            next = '<li><a href="?{}">>></a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param,[self.page + 1])
            next = '<li><a href="?{}">>></a></li>'.format(self.query_dict.urlencode())   
        page_str_list.append(next)

        self.query_dict.setlist(self.page_param,[self.page_num])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        jump_str = '''
                    <li>
                    <form  style = "float:left;margin-left:-1px" method="get">
                    <div class="input-group" style="width: 100px;">
                    <input  style="position:relative;float:left;display:inline-block;width:88px;" class= "form-control" type="text" name = "page">
                    <span class="input-group-btn">
                        <button class="btn btn-default" type="submit">跳转</button>
                    </span>
                    
                    </div>
                    
                    </form>
                    </li>
                '''
        page_str_list.append(jump_str)
        page_string = mark_safe("".join(page_str_list))
        #print(page_string)
        return page_string
