#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from base64 import b64encode

# generate the private and public key
#
# mkdir ~/.pyenc && cd ~/.pyenc
# openssl genrsa -out private.pem 3072
# openssl rsa -pubout -in private.pem -out public.pem -outform PEM


def encrypt(args):
    f = args.file[0]
    in_file = f
    is_dir = False
    if os.access(f, os.R_OK):
        if os.path.isdir(f):
            in_file = f + '.tbz'
            os.popen('tar cjf {} {}'.format(in_file, f))
            is_dir = True
    else:
        print 'File or directory not found'
        exit(1)

    pass_key = b64encode(os.urandom(126))
    key_path = f + '.key'
    with open(key_path, 'w') as key_file:
        key_file.write(pass_key)

    os.popen('openssl enc -e -bf -salt -base64 -pass file:{} -in {} -out {}.enc'.format(key_path, in_file, in_file))
    if is_dir:
        os.unlink(in_file)


def decrypt(args):
    f = args.file[0]
    key_path = f + '.key'
    if not os.access(key_path, os.R_OK):
        print 'Key not found'
        exit(1)

    in_file = f + '.enc'
    out_file = f
    is_dir = False
    if not os.access(in_file, os.R_OK):
        in_file = f + '.tbz.enc'
        out_file = f + '.tbz'
        is_dir = True
        if not os.access(in_file, os.R_OK):
            print 'Encoded data not found'
            exit(1)

    os.popen('openssl enc -d -bf -salt -base64 -pass file:{} -in {} -out {}'.format(key_path, in_file, out_file))
    if is_dir:
        os.popen('tar xjf ' + out_file)
        os.unlink(out_file)

parser = argparse.ArgumentParser(prog='pyenc', description='Encrypt/Decrypt files and folders.')
subparsers = parser.add_subparsers()

parser_enc = subparsers.add_parser('e')
parser_enc.set_defaults(func=encrypt)

parser_dec = subparsers.add_parser('d')
parser_dec.set_defaults(func=decrypt)

parser.add_argument('file', nargs=1)

arguments = parser.parse_args()
arguments.func(arguments)
