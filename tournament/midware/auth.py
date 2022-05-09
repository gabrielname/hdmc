from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMidware(MiddlewareMixin):
    
    def process_request(self,request):
        if request.path_info in ['/visitor_login/','/login/','/image/code/','/index/','/']:
            return
        info_dict = request.session.get('info')
        if not info_dict:
            return redirect('/login')