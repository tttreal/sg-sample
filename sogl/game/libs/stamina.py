import math
from ..models import *
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class UserStaminaInfo():
    max_stamina = 0
    current_stamina = 0

    def from_User(user):
        info = UserStaminaInfo()
        info.max_stamina = settings.STAMINA_MAX_LEVEL_RATE * user.level
        info.current_stamina = user.current_stamina

        return info

def update_stamina(user):
    MAX_STAMINA = settings.STAMINA_MAX_LEVEL_RATE * user.level
    if user.current_stamina >= MAX_STAMINA:
        return False

    if user.last_recovered_at == None:
        user.last_recovered_at = timezone.now()

    minute_interval = math.floor((timezone.now() - user.last_recovered_at).total_seconds() / 60)
    recover_stamina_value = int(minute_interval / settings.STAMINA_RECOVER_TIME_MINUTE)
    user.current_stamina = min(user.current_stamina + recover_stamina_value, MAX_STAMINA)
    if user.current_stamina == MAX_STAMINA:
        user.last_recovered_at = timezone.now()
    else:
        user.last_recovered_at = user.last_recovered_at + timedelta(minutes=recover_stamina_value * settings.STAMINA_RECOVER_TIME_MINUTE)

    return True