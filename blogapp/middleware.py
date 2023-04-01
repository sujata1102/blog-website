'''

syntax to define middleware

def middlewarename(get_response):
    Need to write code that is to be executed only once.
    for any initialization or any configuration.

    def your_function(request):
        code need to be executed before view function is called

        res=get_response(request)

        code to be executed after view is called

        return res
    return your_function
'''

def Blog_middleware(get_response):
    print("Code executed only once for any initialization")

    def blog_function(request):
        print("Code executed before view function is called....")

        res=get_response(request)
        print("Code executed after view function is called...")

        return res
    return blog_function