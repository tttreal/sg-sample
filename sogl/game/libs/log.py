from ..models import *
from ipware import get_client_ip


def user_log(user_id:int, type:UserLog.Type, detail:[], request=None, user_level=0):
    user_log = UserLog()
    user_log.user_id = user_id
    user_log.type = type
    user_log.detail = detail
    user_log.user_level = user_level

    if request:
        user_log.device_info = request.user_agent
        ip_address, is_routable = get_client_ip(request)
        user_log.ip_address = ip_address

    user_log.save()
