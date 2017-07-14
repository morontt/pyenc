# PyEnc

Encrypt/Decrypt files and folders with [OpenSSL](https://www.openssl.org/)

## Installation

Generate the private and public key

```bash
mkdir ~/.pyenc && cd ~/.pyenc
openssl genrsa -out private.pem 3072
openssl rsa -pubout -in private.pem -out public.pem -outform PEM
```

Clone or download repository, install script

```bash
git clone https://github.com/morontt/pyenc.git
cd pyenc
cp pyenc.py ~/bin/pyenc
chmod a+x ~/bin/pyenc
```

### Usage

Encrypt file or folder

```bash
pyenc e testfile
```

Decrypt file or folder

```bash
pyenc d testfile
```
