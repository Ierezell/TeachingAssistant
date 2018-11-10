try:
    with open("./plop.txt") as file:
        param = file.realines()
    print(param)
except FileNotFoundError:
    print("plop")
