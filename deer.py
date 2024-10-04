class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        pass

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        pass

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def parse(string: str):
    commands = []
    cm = None
    tmp = 0
    arg = None
    for c in string:
        # c
        if c == 'し':
            pass
        elif c == 'か':
            # commands
            cm = 0
        elif c == 'の':
            cm = cm * 2 + tmp
            tmp = -1
        elif c == 'こ':
            tmp += 1
        elif c == 'た':
            if arg is None:
                arg = 0
        elif c == 'ん':
            arg += 1
        elif c == '　':
            commands.append((cm, arg))
            cm = None
            arg = None
            tmp = 0
    if cm is not None and arg is not None:
        commands.append((cm, arg))
    return commands


def math(stack: list, f):
    r = stack.pop(len(stack) - 1)
    l = stack.pop(len(stack) - 1)
    stack.append(f(l, r))


def run(commands):
    stack = []
    subs = []
    ad = 0
    labels = {}
    line = 0
    getch = _Getch()
    while line < len(commands):
        com = commands[line]
        c = com[0]
        a = com[1]
        if c == 1:
            print(stack[len(stack) - 1], end='')
        elif c == 2:
            print(chr(stack[len(stack) - 1]), end='')
        elif c == 3:
            tmp = stack[len(stack) - 1]
            stack[len(stack) - 1] = stack[len(stack) - 2]
            stack[len(stack) - 2] = tmp
        elif c == 4:
            stack.pop()
        elif c == 5:
            math(stack, lambda l, r: l + r)
        elif c == 6:
            math(stack, lambda l, r: l - r)
        elif c == 7:
            stack.append(stack[len(stack) - 1])
        elif c == 8:
            stack.append(a)
        elif c == 9:
            math(stack, lambda l, r: l * r)
        elif c == 10:
            math(stack, lambda l, r: (l - l % r) / r)
        elif c == 11:
            math(stack, lambda l, r: l % r)
        elif c == 12:
            ad = stack[len(stack) - 1]
        elif c == 13:
            stack.append(ad)
        elif c == 14:
            labels[a] = line
        elif c == 15:
            subs.append(line)
            line = labels[a]
        elif c == 16:
            line = labels[a]
        elif c == 17:
            top = stack[len(stack) - 1]
            if top == 0:
                line = labels[a]
        elif c == 18:
            top = stack[len(stack) - 1]
            if top < 0:
                line = labels[a]
        elif c == 19:
            line = subs.pop()
        elif c == 20:
            ad = ord(getch())
        elif c == 21:
            s = ''
            ch = getch()
            while ch == '\n':
                s += ch
                ch = getch()
            ad = int(s)
        else:
            ad = c - 22
        line += 1

    # for test
    # p = parse(
    """しかのこのここのこのここのここのここのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのここのここのここのこのここのここのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのこのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのこのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのここのこのここのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのここのこのここのここのこのここのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのここのこのここのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのここのこのこのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのこのこのこのこのこのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのここのここのここのこのここのこのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　
しかのこのここのここのこのここのここのここのしたん　しかのここのここのこのここのしたんたん　しかのここのこのしたんたん　"""


# )
# print(p)
# run(p)
if __name__ == '__main__':
    s = ''
    i = input()
    while i == '':
        s += i
        i = input()
    p = parse(s)
    run(p)
