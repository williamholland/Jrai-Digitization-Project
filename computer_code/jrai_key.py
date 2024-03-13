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
    Ĭ - IW
    ĭ - iw
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
    Ŏ - Ow
    ŏ - ow
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

substitutions = (
    (r'^B[bB](?![Bb])', r'Ƀ'), # exactly 2 bs at the start
    (r'^b[bB](?![Bb])', r'ƀ'),
    (r'^(B[bB])[bB]', r'\1'), # if more than 2 bs, put as entered but ignore final b
    (r'^(b[bB])[bB]', r'\1'),
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
        if key == 27:  # ESC key
            return
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
            #stdscr.addstr(1, 0, word)
            stdscr.addch(chr(key))
            stdscr.refresh()

curses.wrapper(main)
