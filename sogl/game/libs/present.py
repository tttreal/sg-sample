from ..models import *
from .reward import *

class PresentBoxInfo:
    user_present_id = 0
    reward_contents = []
    sent_at = None

    def fetch_present_box_infos(user_id):
        not_received_user_presents = UserPresent.objects.filter(user_id=user_id, received_at__isnull=True)

        present_box_infos = []
        for user_present in not_received_user_presents:
            present_box_info = PresentBoxInfo()
            present_box_info.user_present_id = user_present.id
            present_box_info.reward_contents = RewardContent.from_json_data(user_present.rewards, user_present.amount)
            present_box_info.sent_at = user_present.created_at
            present_box_infos.append(present_box_info)

        return present_box_infos

# プレゼントを開封する
def open_present(user_present):
    give_reward(user_present.user_id, user_present.rewards, user_present.amount)

    user_present.received_at = timezone.now()
    user_present.save()

def send_present(user_id, rewards, amount=1):
    user_present = UserPresent()
    user_present.user_id = user_id
    user_present.rewards = rewards
    user_present.amount = amount

    user_present.save()
    

