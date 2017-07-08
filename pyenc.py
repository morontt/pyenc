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
    if os.access(f, os.R_OK):
        if os.path.isdir(f):
            pass
    else:
        print 'File or directory not found'
        exit(1)

    pass_key = b64encode(os.urandom(126))
    key_path = f + '.key'
    with open(key_path, 'w') as key_file:
        key_file.write(pass_key)

    os.popen('openssl enc -e -bf -salt -base64 -pass file:{} -in {} -out {}.enc'.format(key_path, f, f))


def decrypt(args):
    f = args.file[0]
    key_path = f + '.key'
    in_file = f + '.enc'
    if not os.access(key_path, os.R_OK) or not os.access(in_file, os.R_OK):
        print 'Key or encoded data not found'
        exit(1)

    os.popen('openssl enc -d -bf -salt -base64 -pass file:{} -in {} -out {}'.format(key_path, in_file, f))

parser = argparse.ArgumentParser(prog='pyenc', description='Encrypt/Decrypt files and folders.')
subparsers = parser.add_subparsers()

parser_enc = subparsers.add_parser('e')
parser_enc.set_defaults(func=encrypt)

parser_dec = subparsers.add_parser('d')
parser_dec.set_defaults(func=decrypt)

parser.add_argument('file', nargs=1)

arguments = parser.parse_args()
arguments.func(arguments)
