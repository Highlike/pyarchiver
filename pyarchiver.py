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
class Keybinding:
        if 'y2' in locals():
            win.move(y2, 1)
            win.addstr('     ')

        if c == ord('j') and y < len(dir_list):
            win.move(y, 1)
            win.addstr('   ')
            y += 1
            win.move(y, 1)
            win.addstr("-->")
            win.refresh()
        elif c == ord('k') and y > 1:
            win.move(y, 1)
            win.addstr('   ')
            y -= 1
            win.move(y, 1)
            win.addstr("-->")
            win.refresh()

    def dir_forward():
        elif c == ord('l'):
            if not dir == '':
                new_dir = dir + "/" + dir_list[y - 1]
            else:
                new_dir = dir_list[y - 1]
            main(win, archive, new_dir)

    def dir_back():
        elif c == ord('h'):
            win.erase()
            path_list = dir.split("/")
            new_dir = '/'.join(path_list[:-1])
            main(win, archive, new_dir)

    def extract_item():
        elif c == ord('e'):
            if not dir == '':
                selected_dir = dir + '/' + dir_list[y - 1]
            else:
                selected_dir = dir_list[y - 1]
            extract(archive, selected_dir)
            y2 = len(dir_list) + 2
            win.move(y2, 1)
            win.addstr('done!')
            win.refresh()

    def exit():
        elif c == ord('q'):
            sys.exit()

def initialize(screen, archive):
    win = curses.newwin(10, 90)
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

    while True:
        Keybinding

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
