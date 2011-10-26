#!/usr/bin/env python3

import tarfile
import zipfile
import sys

def determine_filetype(name):
    if tarfile.is_tarfile(name):
        tar(name)
    elif zipfile.is_zipfile(name):
        zip(name)
    else:
        raise ValueError("Not a valid archive type")

def tar(name):
    with tarfile.open(name) as file:
        names = file.getnames()
        current_dir = ''
        new_dir = []
        current_level = 2
        for x in names:
            x_list = x.split('/')
            if len(x_list) == current_level:
                dir = x_list[current_level - 1]
                if dir.startswith(current_dir):
                    new_dir.append(dir) 
        current_level += 1
        print(new_dir)

if __name__ == '__main__':
    script, file = sys.argv
    determine_filetype(file)
