import random
from ..models import *
from .reward import *

class GachaInfo:
    gacha_id = 0
    name = ""
    introduction = ""
    cost_type = ""
    cost_id = 0
    cost_amount = 0
    cost_explanation = 0
    exec_count = 1
    open_at = None
    close_at = None

    def __init__(self, gacha):
        self.gacha_id = gacha.id
        self.name = gacha.name
        self.introduction = gacha.introduction
        self.cost_type = gacha.cost_type
        self.cost_id = gacha.cost_id
        self.cost_amount = gacha.cost_amount
        self.exec_count = gacha.exec_count
        self.open_at = gacha.open_at
        self.close_at = gacha.close_at

    def filter():
        now = timezone.now()
        gachas = Gacha.objects.filter(open_at__lte=now, close_at__gt=now)
        gachas = sorted(list(gachas), key=lambda x: x.display_order, reverse=True)

        gacha_infos = []
        for gacha in gachas:
            gacha_info = GachaInfo(gacha)
            match gacha_info.cost_type:
                case "point":
                    name = Point.objects.get(id=gacha_info.cost_id).name
                    gacha_info.cost_explanation = f"{name}{gacha_info.cost_amount}個"

            gacha_infos.append(gacha_info)

        return gacha_infos

class GachaExecutor:
    gacha_id = 0
    exec_count = 0

    def __init__(self, gacha_id, exec_count):
        self.gacha_id = gacha_id
        self.exec_count = exec_count

    def exec(self):
        gacha_slots = GachaSlot.objects.filter(gacha_id=self.gacha_id)
        gacha_slots = sorted(list(gacha_slots), key=lambda x: x.id)

        res = []

        for _ in range(0, self.exec_count):
            rand_value = random.randrange(1, 10001)
            total_weight = 0
            for gacha_slot in gacha_slots:
                total_weight += gacha_slot.weight
                if rand_value <= total_weight:
                    res.append(gacha_slot)
                    break

        return res
