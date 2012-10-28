from django.core.cache import get_cache

def get_srv(request):
    cache = get_cache('inprocess')
    if 'srv' in request.session:
        key = request.session['srv']
        data = cache.get(key)
        return data
    return None