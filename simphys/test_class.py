class Test():
    def __init__(self):
        pass

essai=Test()

typ=type(essai)

print(typ)

nom=Test

c=nom()
print(c)

def func(classe):
    a=classe()
    return a

b=func(nom)
print(b)