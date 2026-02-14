import datetime

data = {
    "07-09": "Tom Hanks",
    "09-02": "Keanu Reeves",
    "11-11": "Leonardo DiCaprio"
}

def f(x):
    try:
        d = datetime.datetime.strptime(x, "%Y-%m-%d")
        k = d.strftime("%m-%d")
        if k in data:
            return data[k]
        else:
            return None
    except:
        return None

def run():
    print("Welcome")
    n = input("Name: ")
    b = input("Birthdate: ")
    r = f(b)
    if r:
        print("Hello " + n + " actor: " + r)
    else:
        print("Hello " + n + " no match")

run()
