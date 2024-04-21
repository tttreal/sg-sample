class Chara:
    name = 'no name'
    def __init__(self, name):
        self.name = name

def f(chara):
    return chara.name + "1"

chara = Chara('Aman')
print(f(chara))

class PaDChara(Chara):
    pass
    #def __init__(self, name):
    #    super.__init__(name)

print(f(PaDChara('Aman')))
