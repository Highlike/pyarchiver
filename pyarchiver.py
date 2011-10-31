#!/usr/bin/env python3

import tarfile
import zipfile
import sys
import curses

def determine_filetype(name):
    if tarfile.is_tarfile(name):
        return "is_tar"
    elif zipfile.is_zipfile(name):
        return "is_zip"
    else:
        raise ValueError("Not a valid archive type")

def tar_file_list(file, dir):
    if not isinstance(dir, str):
        raise ValueError("This is not a valid directory")
    names = file.getnames()
    if dir.endswith("/"):
        dir = dir[:-1]
    if not dir == "":
        current_level = len(dir.split("/")) + 1
    else:
        current_level = 1
    new_dir = []
    for item in names:
        item_list = item.split("/")
        if len(item_list) == current_level:
            if item.startswith(dir):
                new_dir.append(item_list[-1])
    if len(new_dir) ==  0:
        raise ValueError("Not a valid directory")
    else:
        return sorted(new_dir)

def extract(archive, path):
    member = archive.getmember(path)
    archive.extract(member)

### GUI ###
def initialize(screen, archive):
    win = curses.newwin(10, 90)
    while True:
        main(win, archive)

def main(win, archive, dir=''):
    win.erase()
    try:
        dir_list = tar_file_list(archive, dir)
    except ValueError:
        dir_list = ["Not a valid directory"]
    x = 0
    for item in dir_list:
        x += 1
        win.move(x, 6)
        win.addstr(str(item))

    y = 1
    win.move(y, 1)
    win.addstr("-->")

    win.refresh

    keybinding = Keybinding(win, dir_list, dir, y)
    move = Move()

    c = 0
    while not c == ord('l') or not c == ord('h'):
        c = win.getch()
        if c == ord('j') and y < len(dir_list):
            move.down()
        elif c == ord('k') and y > 1:
            move.up()
        elif c == ord('l'):
            keybinding.dir_forward()
        elif c == ord('h'):
            keybinding.dir_back()
        elif c == ord('e'):
            keybinding.extract_item(archive)
        elif c == ord('q'):
            keybinding.exit()

class Keybinding:
    def __init__(self, win, dir_list, dir, y):
        self.win = win
        self.dir_list = dir_list
        self.dir = dir
        self.y = y

#       if 'y2' in locals():
#           win.move(y2, 1)
#           win.addstr('     ')
#           win.refresh()

    def dir_forward(self):
        if not self.dir == '':
            new_dir = self.dir + "/" + self.dir_list[self.y - 1]
        else:
            new_dir = self.dir_list[self.y - 1]

    def dir_back(self):
        path_list = self.dir.split("/")
        new_dir = '/'.join(path_list[:-1])

    def extract_item(self, archive):
        if not self.dir == '':
            selected_dir = self.dir + '/' + self.dir_list[y - 1]
        else:
            selected_dir = self.dir_list[y - 1]
        extract(archive, selected_dir)
        y2 = len(self.dir_list) + 2
        win.move(y2, 1)
        win.addstr('done!')
        win.refresh()

    def exit(self):
        sys.exit()

class Move(Keybinding):
    def __init__(self):
        pass

    def down(self):
        win.move(y, 1)
        win.addstr('   ')
        y += 1
        win.move(y, 1)
        win.addstr("-->")
        win.refresh()

    def up(self):
        win.move(y, 1)
        win.addstr('   ')
        y -= 1
        win.move(y, 1)
        win.addstr("-->")
### GUI ####

if __name__ == '__main__':
    script, file = sys.argv
    archive = determine_filetype(file)
    if archive == "is_tar":
        with tarfile.open(file) as f:
            curses.wrapper(main, f)
    elif archive == "is_zip":
        with zipfile.open(file) as f:
            curses.wrapper(main, f)
