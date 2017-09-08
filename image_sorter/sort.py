#!/usr/bin/env python3

import os
from os.path import isfile, join, isdir
import sys
import shutil
import cv2
import imghdr
import tqdm

def main():

    if len(sys.argv) != 4:
        print("Usage: ./sort.py [source] [trypophobic] [non_trypophobic]")
        return

    try:
        source_dir = sys.argv[1]
        positive_dir = sys.argv[2]
        negative_dir = sys.argv[3]

        if not isdir(source_dir):
            raise RuntimeError()

        if not isdir(positive_dir):
            os.mkdir(positive_dir)
        if not isdir(negative_dir):
            os.mkdir(negative_dir)


    except Exception as ex:
        print("Malformed args")
        return

    cv2.namedWindow('Trypophobic or not?',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Trypophobic or not?', 1200, 1000)

    filenames_to_sort = [f for f in os.listdir(source_dir) if isfile(join(source_dir, f))]
    for filename in tqdm.tqdm(filenames_to_sort):

        filename_type = imghdr.what(join(source_dir, filename))

        if filename_type == 'gif':
            new_filename = join(source_dir, filename)[:-4]+'.jpeg'
            os.system("convert %s %s"%(join(source_dir, filename), new_filename))
            os.remove(join(source_dir, filename))
            imdata = cv2.imread(new_filename, cv2.IMREAD_COLOR)
        elif filename_type is not None:
            imdata = cv2.imread(join(source_dir, filename), cv2.IMREAD_COLOR)

        cv2.imshow("Trypophobic or not?", imdata)

        response = cv2.waitKey()

        if response == ord('a'):
            shutil.move(join(source_dir, filename), join(positive_dir, filename))

        elif response == ord('l'):
            shutil.move(join(source_dir, filename), join(negative_dir, filename))

        elif response == 27:
            break




if __name__=='__main__':
    main()
