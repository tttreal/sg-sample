from src.model.manager import Manager

class Model():
    id = 0

    objects = None  # マネージャのプレースホルダー

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"{cls}クラスを objects に登録するよ")
        cls.objects = Manager(cls)  # サブクラスごとにマネージャインスタンスを生成


