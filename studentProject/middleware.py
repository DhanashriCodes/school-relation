def disableCSRFCheck(get_response):
    def middleware(request):
        request._dont_enforce_csrf_checks = True
        response = get_response(request)
        return response
    
    return middleware