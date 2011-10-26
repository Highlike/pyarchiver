#!/usr/bin/env python3

import tarfile
import zipfile
import sys

def determine_filetype(name):
    if tarfile.is_tarfile(name):
        return "is_tar"
    elif zipfile.is_zipfile(name):
        return "is_zip"
    else:
        raise ValueError("Not a valid archive type")

def tar(name):
    with tarfile.open(name) as file:
        tar_file_list(file)


def tar_file_list(file, dir):
    if not isinstance(dir, str):
        raise ValueError("This is not a valid directory")
    names = file.getnames()
    new_dir = []
    current_level = len(dir.split("/")) 
    for item in names:
        item_list = item.split('/')
        if len(item_list) == current_level:
            dir2 = item_list[current_level - 1]
            if item.startswith(dir):
                new_dir.append(dir) 
        current_level += 1
        return new_dir

if __name__ == '__main__':
    script, file = sys.argv
