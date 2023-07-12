from datetime import datetime

def prepare_request_log(request):
    return {
        'url': request.build_absolute_uri(),
        'method': request.method,
        'timestamp': datetime.now().strftime('%Y.%m.%d_%H:%M:%S'),
        'body': request.body,
        'headers': request.headers,
        'meta': request.META,
    }