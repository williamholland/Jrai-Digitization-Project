'''

like telex input for vietnamese but for jrai. Differences to Vietnaemse:

* Ƀ and ƀ which should logically be BB and bb to match vietnamese dd
* c and n with caron which I've decided are cc and nn (ch and nh was an option but there are times a user might want ch and nh for loan words)
* dấu móc and breve can appear together, so I've decided s for breve (as they're very common and s in on the home row for qwerty) w for dấu móc and x for both
* combination of breve with circumflex on o, this extends logically

Here is the mapping of input
ascii characters to output jrai characters (note that the case of the second
letter doesn't matter):

    A - A
    a - a
    Ă - AS
    ă - as
    Â - AA
    â - aa
    B - B
    b - b
    Ƀ - BB
    ƀ - bB
    Č - CC
    č - cc
    D - D
    d - d
    Đ - DD
    đ - dd
    E - E
    e - e
    Ĕ - ES
    ĕ - es
    Ê - EE
    ê - ee
    Ê̆ - EX/EWS/ESW
    ê̆ - ex/ews/esw
    G - G
    g - g
    H - H
    h - h
    I - I
    i - i
    Ĭ - IS
    ĭ - is
    J - J
    j - j
    K - K
    k - k
    L - L
    l - l
    M - M
    m - m
    N - N
    n - n
    Ñ - NN
    ñ - nn
    O - O
    o - o
    Ŏ - OS
    ŏ - os
    Ô - OO
    ô - oo
    Ô̆ - OOS/OSO
    ô̆ - oos/oso
    Ơ - OW
    ơ - ow
    Ơ̆ - OWS/OX
    ơ̆ - ows/ox
    P - P
    p - p
    R - R
    r - r
    S - S
    s - s
    T - T
    t - t
    U - U
    u - u
    Ŭ - US
    ŭ - us
    Ư - UW
    ư - uw
    Ư̆ - UWS
    ư̆ - uws
    W - W
    w - w
    Y - Y
    y - y

'''

import re
import curses

ESC_KEY = 27

substitutions = (


    (r'(?<![Aa])A[Ss](?![Ss])', r'Ă'), # AS makes, with exactly 1 s sub
    (r'(?<![Aa])a[Ss](?![Ss])', r'ă'),
    (r'([Aa][Ss])[Ss]', r'\1'), # if more than 2 s, put as entered but ignore final s

    # duplicate of ă because I keep doing this by mistake
    (r'(?<![Aa])A[Ww](?![Ww])', r'Ă'),
    (r'(?<![Aa])a[Ww](?![Ww])', r'ă'),
    (r'([Aa][Ww])[Ww]', r'\1'),

    (r'(?<![Aa])A[Aa](?![Aa])', r'Â'),
    (r'(?<![Aa])a[Aa](?![Aa])', r'â'),
    (r'([Aa][Aa])[Aa]', r'\1'),


    (r'B[bB](?![Bb])', r'Ƀ'), # exactly 2 bs
    (r'b[bB](?![Bb])', r'ƀ'),
    (r'([bB]{2})[bB]', r'\1'), # if more than 2 bs, put as entered but ignore final b

    (r'C[Cc](?![Cc])', r'Č'),
    (r'c[Cc](?![Cc])', r'č'),
    (r'([Cc]{2})[Cc]', r'\1'),

    (r'D[Dd](?![Dd])', r'Đ'),
    (r'd[Dd](?![Dd])', r'đ'),
    (r'([Dd]{2})[Dd]', r'\1'),


    (r'(?<![Ee])E([Ee][Ss]|[Ss][Ee])(?![EeSs])', r'Ê̆'),
    (r'(?<![Ee])e([Ee][Ss]|[Ss][Ee])(?![EeSs])', r'ê̆'),
    (r'([Ee][EeSs]{2})[EeSs]', r'\1'),

    (r'(?<![Ee])E[Ss](?![Ss])', r'Ĕ'),
    (r'(?<![Ee])e[Ss](?![Ss])', r'ĕ'),
    (r'(?<![Ee])([Ee][Ss])[Ss]', r'\1'),

    (r'(?<![Ee])E[Ee](?![Ee])', r'Ê'),
    (r'(?<![Ee])e[Ee](?![Ee])', r'ê'),
    (r'([Ee]{2})[Ee]', r'\1'),


    (r'(?<![Ii])I[Ss](?![Ss])', r'Ĭ'),
    (r'(?<![Ii])i[Ss](?![Ss])', r'ĭ'),
    (r'([Ii][Ss])[Ss]', r'\1'),


    (r'N[Nn](?![Nn])', r'Ñ'),
    (r'n[Nn](?![Nn])', r'ñ'),
    (r'([Nn]{2})[Nn]', r'\1'),


    (r'(?<![Oo])O([Oo][Ss]|[Ss][Oo])(?![OoSs])', r'Ô̆'),
    (r'(?<![Oo])o([Oo][Ss]|[Ss][Oo])(?![OoSs])', r'ô̆'),
    (r'([Oo][OoSs]{2})[OoSs]', r'\1'),

    (r'O([Ww][Ss]|[Ss][Ww])(?![SsWwOo])', r'Ơ̆'),
    (r'o([Ww][Ss]|[Ss][Ww])(?![SsWwOo])', r'ơ̆'),
    (r'([Oo][OoSsWw]{2})[OoSsWw]', r'\1'),

    (r'(?<![Oo])O[Ss](?![Ss])', r'Ŏ'),
    (r'(?<![Oo])o[Ss](?![Ss])', r'ŏ'),
    (r'([Oo][Ss])[Ss]', r'\1'),

    (r'(?<![Oo])O[Oo](?![Oo])', r'Ô'),
    (r'(?<![Oo])o[Oo](?![Oo])', r'ô'),
    (r'([Oo]{2})[Oo]', r'\1'),

    (r'O[Ww](?![Ww])', r'Ơ'),
    (r'o[Ww](?![Ww])', r'ơ'),
    (r'([Oo][Ww])[Ww]', r'\1'),


    (r'(?<![Uu])U([Ww][Ss]|[Ss][Ww])(?![SsWwUu])', r'Ư̆'),
    (r'(?<![Uu])u([Ww][Ss]|[Ss][Ww])(?![SsWwUu])', r'ư̆'),
    (r'([Uu][UuSsWw]{2})[UuSsWw]', r'\1'),

    (r'(?<![Uu])U[Ss](?![Ss])', r'Ŭ'),
    (r'(?<![Uu])u[Ss](?![Ss])', r'ŭ'),
    (r'([Uu][Ss])[Ss]', r'\1'),

    (r'(?<![Uu])U[Ww](?![Ww])', r'Ư'),
    (r'(?<![Uu])u[Ww](?![Ww])', r'ư'),
    (r'([Uu][Ww])[Ww]', r'\1'),
)

def process_word(word):
    ''' given a word, do all the substitutions and return the new jrai word '''
    for s in substitutions:
        if re.search(s[0], word):
            word = re.sub(s[0], s[1], word)
    return word

def main(stdscr):

    stdscr.clear()
    stdscr.addstr(0, 0, "Type Jrai (Press ESC to exit): ")
    stdscr.move(1, 0)
    stdscr.refresh()

    prev_words = ''
    word = ''

    while True:
        key = stdscr.getch()
        if key == ESC_KEY:
            return prev_words+word
        elif key == curses.KEY_BACKSPACE:
            if word:
                word = word[:-1]
                stdscr.move(stdscr.getyx()[0], max(0, stdscr.getyx()[1] - 1))
                stdscr.delch()
                stdscr.refresh()
            elif prev_words:
                prev_words = prev_words[:-1]
                stdscr.move(stdscr.getyx()[0], max(0, stdscr.getyx()[1] - 1))
                stdscr.delch()
                stdscr.refresh()
        elif key != curses.KEY_RESIZE and not chr(key).isalpha():
            # if pressed a nonalphabetic letter, time to convert the word
            word = process_word(word)
            stdscr.move(1, 0)
            stdscr.clrtoeol()
            prev_words += word
            prev_words += chr(key)
            stdscr.addstr(1, 0, prev_words)
            stdscr.refresh()
            word = ""
        else:
            word += chr(key)
            stdscr.addch(chr(key))
            stdscr.refresh()

print(curses.wrapper(main))
