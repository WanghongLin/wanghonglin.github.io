#!/usr/bin/env python
# -*-: coding: utf-8 -*-

import argparse
import os
import re
import base64


IMG_PATTERN = re.compile('(img|幻灯片)\\d+\\.jpe?g', re.IGNORECASE)
IMG_TAG = '<img class="section" src="data:image/jpeg;base64,{src}">'
RM_PATTERN = re.compile('(img|text|thumb)\\d+\\.(jpe?g|html)')


def find_img_and_generate(folder, title, template, output):
    if folder and os.path.isdir(folder):
        images = []
        for fn in sorted(os.listdir(folder), key=lambda x: int(re.sub('\\D', '', x))):
            if IMG_PATTERN.match(fn):
                with open(os.path.join(folder, fn), 'rb') as fp:
                    s = base64.encodebytes(fp.read()).decode('ascii')
                    img = IMG_TAG.format(src=s)
                    images.append(img)

        with open(template, 'r') as tf:
            with open(output, 'w') as wf:
                wf.write(tf.read() % (title, '\n'.join(images)))

        if args.clean:
            for f in os.listdir(folder):
                if RM_PATTERN.match(f):
                    os.unlink(os.path.join(folder, f))

def create_all_card():
    lis = []
    for d in os.scandir('./ppt'):
        if os.path.isdir(d):
            find_img_and_generate(folder=os.path.join('ppt', d.name), title=d.name,
                                  template='template.html', output=os.path.join('card', '%s.html' % d.name))
            link = '%s.html' % d.name
            name = d.name.replace('_', ' ').capitalize()
            li = '\t\t<li><a href="{0}">{1}</a></li>'.format(link, name)
            print(li)
            lis.append(li)
    with open('flashcard.html', 'r') as rfp:
        with open('card/index.html', 'w') as wfp:
            wfp.write(rfp.read() % '\n'.join(lis))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a flash card html for mnemonic')
    parser.add_argument('--folder', type=str, default='.', required=False, help='Input directory')
    parser.add_argument('--title', type=str, default='Flash card', required=False, help='Title of document')
    parser.add_argument('--template', type=str, default='template.html', required=False, help='Input template')
    parser.add_argument('--output', type=str, default='flashcard.html', required=False, help='Output file name')
    parser.add_argument('--auto', action='store_true', default=False, required=False, help='Run in auto mode, create all card in ppt directory')
    parser.add_argument('--clean', action='store_true', default=False, required=False, help='Clean source directory after generate')
    args = parser.parse_args()
    if args.auto:
        create_all_card()
    else:
        find_img_and_generate(**vars(args))
