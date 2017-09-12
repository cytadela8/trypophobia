#!/usr/bin/env python3

import cv2
import os
import sys
from PIL import Image
import numpy as np
from hashlib import md5
import shutil
import tqdm
import random
import string

def main():

    if len(sys.argv) != 3:
        print("Usage: ./normalize [directory] [targetdir]")
        return
    try:
        source_dir = sys.argv[1]
        dest_dir = sys.argv[2]
        if not os.path.isdir(source_dir):
            raise RuntimeError()
        if not os.path.isdir(dest_dir):
            os.mkdir(dest_dir)
    except:
        print("Malformed args")
        return

    filenames = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    tmpfile = 'tmp/tmp' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    for filename in tqdm.tqdm(filenames):
        path_to_file = os.path.join(source_dir, filename)

        rawdata = np.array(Image.open(path_to_file).convert("RGB"))
        rawdata = cv2.cvtColor(rawdata, cv2.COLOR_RGB2BGR)

        height = rawdata.shape[1]
        width = rawdata.shape[0]

        factor_h = 256/height
        factor_w = 256/width
        factor = max(factor_h, factor_w)
        rawdata = cv2.resize(rawdata, (round(height*factor), round(width*factor)))

        height = rawdata.shape[1]
        width = rawdata.shape[0]
        posh = int(float(height)/2-256/2)
        posw = int(float(width)/2-256/2)

        cv2.imwrite(tmpfile, rawdata[posw:(posw+256), posh:(posh+256), :])
        hash = md5(open(tmpfile, 'rb').read()).hexdigest()

        dest_path = os.path.join(dest_dir, hash+".png")
        shutil.move(tmpfile, dest_path)

        #print("%s\t=>\t%s"%(path_to_file,dest_path))

    return

if __name__=="__main__":
    main()
