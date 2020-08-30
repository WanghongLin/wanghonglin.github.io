#!/usr/bin/env python
# -*-: coding: utf-8 -*-

import argparse
import os
import re
import base64


IMG_PATTERN = re.compile('img\d+\.jpe?g')
IMG_TAG = '<img src="data:image/jpeg;base64,{src}">'
RM_PATTERN = re.compile('(img|text|thumb)\d+\.(jpe?g|html)')


def find_img_and_generate(folder, title, template, output):
    if folder and os.path.isdir(folder):
        images = []
        for fn in sorted(os.listdir(folder)):
            if IMG_PATTERN.match(fn):
                with open(fn, 'rb') as fp:
                    s = base64.encodestring(fp.read())
                    img = IMG_TAG.format(src=s)
                    images.append(img)

        with open(template, 'r') as tf:
            with open(output, 'w') as wf:
                wf.write(tf.read() % (title, '\n'.join(images)))

        for f in os.listdir(folder):
            if RM_PATTERN.match(f):
                os.unlink(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a flash card html for mnemonic')
    parser.add_argument('--folder', type=str, default='.', required=False, help='Input directory')
    parser.add_argument('--title', type=str, default='Flash card', required=False, help='Title of document')
    parser.add_argument('--template', type=str, default='template.html', required=False, help='Input template')
    parser.add_argument('--output', type=str, default='flashcard.html', required=False, help='Output file name')
    args = parser.parse_args()
    find_img_and_generate(**vars(args))
