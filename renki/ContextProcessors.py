from renki.utils import get_srv

def user_information(request):
    retval = {}
    srv = get_srv(request)
    if srv:
        retval['login_username'] = srv.username
    return retval