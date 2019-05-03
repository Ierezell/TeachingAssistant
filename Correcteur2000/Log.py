"""REQUIRED pip install colored"""

from colored import fg, bg, attr
import tqdm


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


def print_wtf(msgWTF):
    tqdm.tqdm.write(show(msgWTF, f=BLUE, b=MAGENTA))


def print_note(resultat, ponderation):
    if resultat == ponderation:
        tqdm.tqdm.write(
            f'{show("    Note :", f=WHITE)} {show(resultat, f=GREEN)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')
    elif resultat <= ponderation/2:
        tqdm.tqdm.write(
            f'{show("    Note :", f=WHITE)} {show(resultat, f=RED)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')
    else:
        tqdm.tqdm.write(f'{show("    Note :", f=WHITE)} {show(resultat, f=YELLOW)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')


def print_failing(msg, *, limit=1000):
    if len(msg) > limit:
        tqdm.tqdm.write(f'        {show(" Message trop long ", b=MAGENTA, f=WHITE)}')
    else:
        tqdm.tqdm.write(f'        {show(msg, f=RED)}')


def print_passing(msg, *, limit=1000):
    if len(msg) > limit:
        tqdm.tqdm.write(f'        {show(" Message trop long ", b=MAGENTA, f=WHITE)}')
    else:
        tqdm.tqdm.write(f'        {show(msg, f=GREEN)}')


def print_warning(msg):
    tqdm.tqdm.write(show(msg, f=YELLOW))


def print_ok(x):
    tqdm.tqdm.write(show(x, f=BLUE))


def print_command(nomFichier, Arguments):
    tqdm.tqdm.write(f'      {show(nomFichier)} {show(Arguments, f=ORANGE)}')


def print_titre(nomDuTest):
    tqdm.tqdm.write(f'    {show(nomDuTest, f=MAGENTA)}')


def print_equipe(GroupNb):
    tqdm.tqdm.write(show(f'  ÉQUIPE {GroupNb}\n', f=WHITE))


def print_final(critere, resultat, ponderation):
    if resultat == ponderation:
        tqdm.tqdm.write(
            f'{show(f"  Critère {critere} :", f=WHITE)} {show(resultat, f=GREEN)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')
    elif resultat <= ponderation/2:
        tqdm.tqdm.write(
            f'{show(f"  Critère {critere} :", f=WHITE)} {show(resultat, f=RED)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')
    else:
        tqdm.tqdm.write(f'{show(f"  Critère {critere} :", f=WHITE)} {show(resultat, f=YELLOW)}{show("/", f=WHITE)}{show(ponderation, f=GREEN)}\n')


def print_barre():
    tqdm.tqdm.write(show(' '*100+'\n', b=WHITE))
