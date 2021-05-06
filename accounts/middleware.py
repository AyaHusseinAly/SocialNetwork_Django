from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import resolve
from django.conf import settings
class AnonymousMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        route_name = resolve(request.path_info).url_name
        if request.user.is_anonymous:
            if route_name in settings.AUTH_EXEMPT_ROUTES or request.path == '/admin/':
                return self.get_response(request)
            else:
                return redirect('/login/')
        return self.get_response(request)
        