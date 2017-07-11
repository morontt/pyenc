#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from base64 import b64encode, b64decode

import rsa


def chunk_split(s, l):
    res = '\n'.join(s[i:min(i + l, len(s))] for i in xrange(0, len(s), l))
    return res + '\n'


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

    public_keydata = ''

    try:
        with open(os.path.expanduser('~/.pyenc/public.pem'), mode='rb') as public_file:
            public_keydata = public_file.read()
    except IOError:
        print 'Public key not found'
        exit(1)

    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_keydata)

    pass_key = b64encode(os.urandom(126))
    key_path = f + '.k'
    with open(key_path, 'w') as key_file:
        key_file.write(pass_key)

    os.popen('openssl enc -e -bf -salt -base64 -pass file:{} -in {} -out {}.enc'.format(key_path, in_file, in_file))
    if is_dir:
        os.unlink(in_file)

    encoded_key = b64encode(rsa.encrypt(pass_key, public_key))
    encoded_key_path = f + '.key'
    with open(encoded_key_path, 'w') as encoded_key_file:
        encoded_key_file.write(chunk_split(encoded_key, 64))
    os.unlink(key_path)


def decrypt(args):
    f = args.file[0]
    encoded_key_path = f + '.key'
    if not os.access(encoded_key_path, os.R_OK):
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

    private_keydata = ''

    try:
        with open(os.path.expanduser('~/.pyenc/private.pem'), mode='rb') as private_file:
            private_keydata = private_file.read()
    except IOError:
        print 'Private key not found'
        exit(1)

    private_key = rsa.PrivateKey.load_pkcs1(private_keydata)

    key_path = f + '.k'
    with open(encoded_key_path, 'r') as encoded_key_file:
        pass_key = rsa.decrypt(b64decode(encoded_key_file.read()), private_key)
        with open(key_path, 'w') as key_file:
            key_file.write(pass_key)

    os.popen('openssl enc -d -bf -salt -base64 -pass file:{} -in {} -out {}'.format(key_path, in_file, out_file))
    if is_dir:
        os.popen('tar xjf ' + out_file)
        os.unlink(out_file)
    os.unlink(key_path)

parser = argparse.ArgumentParser(prog='pyenc', description='Encrypt/Decrypt files and folders.')
subparsers = parser.add_subparsers()

parser_enc = subparsers.add_parser('e')
parser_enc.set_defaults(func=encrypt)

parser_dec = subparsers.add_parser('d')
parser_dec.set_defaults(func=decrypt)

parser.add_argument('file', nargs=1)

arguments = parser.parse_args()
arguments.func(arguments)
