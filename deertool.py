def get(c):
    st = bin(ord(c) + 22)
    r = 'しかの'
    for s in st:
        if s == '0':
            r += 'この'
        if s == '1':
            r += 'ここの'
    r += 'したん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　'
    return r


def gets(string):
    for s in string:
        g = get(s)
        print(g)


if __name__ == '__main__':
    gets(input())
