from typing import Any
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from inflection import underscore

class CustomManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

class BaseModel(models.Model):
    objects = CustomManager()  # カスタムマネージャーをデフォルトに設定

    # ここで created_at, updated_at を定義したかったが、カラムの順番が後ろにならなかった
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # 抽象クラスとして設定
        db_table = "aaa" # この文字列がテーブル名になる。djangoのデフォルトだとアプリ名が接頭語に付き、クラス名が続く。例えばgame_userなど

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # テーブル名をクラス名のcamel_caseにする
        cls.Meta.db_table = underscore(cls.__name__)

        ## updated_at, created_atフィールドを最後に追加 -> だめだった
        #cls.add_to_class('updated_at', models.DateTimeField(auto_now=True))
        #cls.add_to_class('created_at', models.DateTimeField(auto_now_add=True))

# Create your models here.
# TODO index
# TODO unique制約
class User(BaseModel):
    name = models.CharField(max_length=8)
    level = models.IntegerField(default=1)
    login_count = models.IntegerField(db_comment="The number of logins")
    last_accessed_at = models.DateTimeField(null=True)
    current_stamina = models.IntegerField(default=0)
    last_recovered_at = models.DateTimeField(default=timezone.now)
    select_party_id = models.BigIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Chara(BaseModel):
    name = models.CharField(max_length=100)
    power = models.IntegerField()
    power_rate_by_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserChara(BaseModel):
    user_id = models.BigIntegerField()
    chara_id = models.BigIntegerField()
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def enhance(self, level):
        self.level = level

class Point(BaseModel):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserPoint(BaseModel):
    user_id = models.BigIntegerField()
    point_id = models.BigIntegerField()
    amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def updateAmount(self, amount_delta):
        self.amount = self.amount + amount_delta

class Party(BaseModel):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserParty(BaseModel):
    user_id = models.BigIntegerField()
    party_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserPartyChara(BaseModel):
    user_party_id = models.BigIntegerField()
    user_chara_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Quest(BaseModel):
    class Type(models.TextChoices):
        NORMAL = 'normal', '定常クエスト',
        EVENT = 'event', 'イベントクエスト',

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=Type.choices, default=Type.NORMAL)
    power = models.BigIntegerField()
    display_order = models.IntegerField()
    need_stamina = models.IntegerField()
    rewards = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserQuest(BaseModel):
    quest_id = models.BigIntegerField()
    user_id = models.BigIntegerField(default=0)
    is_clear = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserPresent(BaseModel):
    user_id = models.BigIntegerField()
    rewards = models.JSONField()
    amount = models.IntegerField()
    received_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Gacha(BaseModel):
    name = models.CharField(max_length=100)
    introduction = models.CharField(max_length=1000)
    display_order = models.IntegerField()
    cost_type = models.CharField(max_length=100)
    cost_id = models.BigIntegerField()
    cost_amount = models.IntegerField()
    exec_count = models.IntegerField(default=1)
    open_at = models.DateTimeField()
    close_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GachaSlot(BaseModel):
    gacha_id = models.BigIntegerField()
    weight = models.IntegerField(db_comment="permyriad, 万分率", validators=[MinValueValidator(0), MaxValueValidator(10000)])
    rewards = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LoginBonus(BaseModel):
    name = models.CharField(max_length=100)
    open_at = models.DateTimeField()
    close_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LoginBonusReward(BaseModel):
    login_bonus_id = models.BigIntegerField()
    day = models.IntegerField()
    rewards = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserLoginBonus(BaseModel):
    user_id = models.BigIntegerField()
    login_bonus_id = models.BigIntegerField()
    day = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Announce(BaseModel):
    title = models.CharField(max_length=100)
    body = models.TextField()
    open_at = models.DateTimeField()
    close_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Mission(BaseModel):
    CONDITION_TYPE_CHOICES = [
        ('login_count', 'ログイン回数'),
        ('clear_quest', 'クエストクリア'),
    ]

    name = models.CharField(max_length=200)
    condition_type = models.CharField(max_length=100, choices=CONDITION_TYPE_CHOICES)
    condition_value = models.IntegerField()
    target_amount = models.IntegerField()
    rewards = models.JSONField()
    open_at = models.DateTimeField()
    close_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserMission(BaseModel):
    user_id = models.BigIntegerField()
    mission_id = models.BigIntegerField()
    count = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    is_rewarded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(BaseModel.Meta):
        unique_together = ('user_id', 'mission_id')

class UserLog(BaseModel):
    class Type(models.TextChoices):
        DAILY_LOGIN = 'daily_login', 'ログイン',
        QUEST = 'quest', 'クエスト',
        MISSION_COMPLETE = 'mission_complete', 'ミッション達成',

    user_id = models.BigIntegerField()
    type = models.CharField(max_length=50, choices=Type.choices)
    device_info = models.CharField(max_length=255, null=True, blank=True)
    detail = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_level = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Event(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    ranking_point_id = models.BigIntegerField()
    open_at = models.DateTimeField()
    close_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserEvent(BaseModel):
    user_id = models.BigIntegerField()
    event_id = models.BigIntegerField()
    score = models.IntegerField(default=0)
    is_rewarded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(BaseModel.Meta):
        unique_together = ('user_id', 'event_id')

class EventReward(BaseModel):
    event_id = models.BigIntegerField()
    rank_from = models.IntegerField()
    rank_to = models.IntegerField()
    rewards = models.JSONField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EventQuest(BaseModel):
    event_id = models.BigIntegerField()
    quest_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(BaseModel.Meta):
        unique_together = ('event_id', 'quest_id')
