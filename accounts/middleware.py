from django.http import HttpResponseForbidden
from django.shortcuts import redirect
class AnonymousMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        
        if request.path == "logout":
            return redirect('profile')
            
        return self.get_response(request)
            # return HttpResponseForbidden("NO")
