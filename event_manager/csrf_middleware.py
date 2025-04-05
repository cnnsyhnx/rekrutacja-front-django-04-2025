class CsrfFixMiddleware:
    """
    Custom middleware to address CSRF issues in the environment.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Ensure CSRF cookie is properly set
        if not request.COOKIES.get('csrftoken'):
            response.set_cookie('csrftoken', request.META.get('CSRF_COOKIE', ''), 
                               secure=True, samesite='None')
        
        return response