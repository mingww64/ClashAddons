import inspect


class Colors:
    # SGR color constants
    # rene-d 2018
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"


def whoami():
    return inspect.stack()[2][3]


def whosdaddy():
    if '<module>' in inspect.stack()[3][3]:
        return inspect.stack()[3][1]
    return inspect.stack()[3][3]


def Shell(t, *r):
    t = str(t)
    r = ''.join(map(str, r))
    print(Colors.GREEN+f"Shell:{whoami()}\t" +
          Colors.LIGHT_GREEN+t+Colors.CYAN+r+Colors.END)


def Skip(t, *r):
    t = str(t)
    r = ''.join(map(str, r))
    print(Colors.FAINT+Colors.CYAN+f"Skip:{whoami()}\t" +
          Colors.LIGHT_CYAN+t+Colors.LIGHT_WHITE+r+Colors.END)


def Info(t, *r):
    t = str(t)
    r = ''.join(map(str, r))
    print(Colors.BLUE+f"Info:{whoami()}\t"+Colors.LIGHT_BLUE +
          t+Colors.LIGHT_PURPLE+r+Colors.END)


def Warn(t, *r):
    t = str(t)
    r = ''.join(map(str, r))
    print(Colors.NEGATIVE+Colors.BROWN+f"Warning:{whoami()}\t" +
          Colors.YELLOW+t+Colors.LIGHT_WHITE+r+Colors.END)


def Debug(t, *r):
    t = str(t)
    r = ''.join(map(str, r))
    print(Colors.NEGATIVE+Colors.BOLD+Colors.BROWN+f"Debug:{whoami()} from {whosdaddy()}\t" +
          Colors.YELLOW+t+Colors.LIGHT_WHITE+r+Colors.END)


def Error(t, *r):
    t = str(t)
    r = ''.join(map(str, r))
    print(Colors.NEGATIVE+Colors.RED+f"Error:{whoami()} from {whosdaddy()}\t"+Colors.BLINK+t +
          Colors.END+Colors.UNDERLINE+Colors.LIGHT_RED+r+Colors.END)
