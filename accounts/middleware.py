from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import resolve
from django.conf import settings
class AnonymousMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # if request.path=='/login/' or request.path=='/signup/' or request.path=='':
        #     return self.get_response(request)
        
        # if request.user.is_anonymous:
        #     return redirect('redirecting')
        current_route_name = resolve(request.path_info).url_name
        if request.user.is_anonymous:
            if current_route_name in settings.AUTH_EXEMPT_ROUTES:
                return self.get_response(request)
            else:
                return redirect('/login/')
        return self.get_response(request)
        
            # return HttpResponseForbidden("NO")
