from src.adapter import local_csv
import inflection

class Manager:

    def __init__(self, model_class):
        self.model_class = model_class

    @staticmethod
    def getAdapter():
        # TODO とりあえずローカルファイル限定
        return local_csv.LocalCSV()

    def get(self, **kwargs):
        # ここではシンプルな例として、IDに基づいてインスタンスを返すダミーの実装をします。
        # 実際にはデータベースからデータを取得するロジックが必要です。
        print(f"Getting {self.model_class.__name__} with {kwargs}")

        adapter = Manager.getAdapter()
        src = inflection.underscore(self.model_class.__name__)
        id = kwargs['id']
        row = adapter.loadById(src, id)

        if row is None:
            return None
        
        obj = self.model_class()
        for k in row:
            setattr(obj, k, row[k])
        print(vars(obj))
