#!/usr/bin/env python3.6

from sys import exit
from os import listdir
from subprocess import run, CalledProcessError

LETSENCRYPT_LIVE = "/etc/letsencrypt/live"
HAPROXY_CERTS = "/etc/haproxy/certs"

try:
    run("certbot renew --dry-run --agree-tos --non-interactive --preferred-challenges http --http-01-port 54321", shell=True, check=True)
except CalledProcessError:
    print("Error renewing certificates")
    exit(1)

for site in listdir(LETSENCRYPT_LIVE):
    try:
        run(f"cd {LETSENCRYPT_LIVE}/{site}", shell=True, check=True)
        run(f"cat fullchain.pem privkey.pem > {HAPROXY_CERTS}/{site}.pem", shell=True, check=True)
    except CalledProcessError:
        print(f"Error combining pem file for site {site}")

try:
    run("service haproxy reload", shell=True, check=True)
except CalledProcessError:
    print("Error reloading haproxy")
    exit(1)
