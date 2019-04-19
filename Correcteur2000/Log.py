"""REQUIRED pip install colored"""

from colored import fg, bg, attr


BLACK = 0
RED = 9
GREEN = 10
YELLOW = 11
BLUE = 12
MAGENTA = 13
GRAY = 7
WHITE = 15
ORANGE = 214
END = attr(0)


def show(x, *, f=GRAY, b=BLACK):
    return f"""{fg(f)}{bg(b)}{x}{END}"""


def wtf(msgWTF):
    print(show(msgWTF, f=BLUE, b=MAGENTA))


def note(resultat, ponderation):
    if resultat == ponderation:
        print(
            f'{show("    Note :", f=WHITE)} {show(resultat, f=GREEN)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')
    elif resultat <= ponderation/2:
        print(
            f'{show("    Note :", f=WHITE)} {show(resultat, f=RED)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')
    else:
        print(f'{show("    Note :", f=WHITE)} {show(resultat, f=YELLOW)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')


def failing(msg):
    print(f'        {show(msg, f=RED)}')


def passing(msg, *, limit=1000):
    if len(msg) > limit:
        print(f'        {show(" Message trop long ", b=MAGENTA, f=WHITE)}')
    else:
        print(f'        {show(msg, f=GREEN)}')


def warning(msg):
    print(show(msg, f=YELLOW))


def ok(x):
    print(show(x, f=BLUE))


def command(nomFichier, Arguments):
    print(f'      {show(nomFichier)} {show(Arguments, f=ORANGE)}')


def titre(nomDuTest):
    print(f'    {show(nomDuTest, f=MAGENTA)}')


def equipe(GroupNb):
    print(show(f'  ÉQUIPE {GroupNb}\n', f=WHITE))


def final(critere, resultat, ponderation):
    if resultat == ponderation:
        print(
            f'{show(f"  Critère {critere} :", f=WHITE)} {show(resultat, f=GREEN)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')
    elif resultat <= ponderation/2:
        print(
            f'{show(f"  Critère {critere} :", f=WHITE)} {show(resultat, f=RED)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')
    else:
        print(f'{show(f"  Critère {critere} :", f=WHITE)} {show(resultat, f=YELLOW)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')


def barre():
    print(show(' '*100+'\n', b=WHITE))
