#!/usr/bin/env python3

from sys import exit,version_info
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
        site_dir = "{}/{}".format(LETSENCRYPT_LIVE, site)
        print("Changing to directory {}".format(site_dir))
        run("cd {}".format(site_dir), shell=True, check=True)
        print("Creating combined pem file")
        run("cat fullchain.pem privkey.pem > {}/{}.pem".format(HAPROXY_CERTS, site), shell=True, check=True)
    except CalledProcessError:
        print("Error combining pem file for site {}".format(site))

try:
    print("Reloading haproxy")
    run("service haproxy reload", shell=True, check=True)
except CalledProcessError:
    print("Error reloading haproxy")
    exit(1)
