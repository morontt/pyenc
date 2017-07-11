# PyEnc

Encrypt/Decrypt files and folders with [OpenSSL](https://www.openssl.org/)

## Usage

Generate the private and public key

```bash
mkdir ~/.pyenc && cd ~/.pyenc
openssl genrsa -out private.pem 3072
openssl rsa -pubout -in private.pem -out public.pem -outform PEM
```
