#!/usr/bin/env python3

import re
import os
import sys
import argparse
import datetime

from sys import stderr
from datetime import date

release_number_regex = r"CFG_RELEASE_NUM[ ]*=[ ]*(?P<value>.*)"

def build_args():
    parser = argparse.ArgumentParser(description='PKGBUILD generator for Rust nightly')
    parser.add_argument('template',
                        type=str,
                        help='Path to PKGBUILD template',
                        metavar='pkgbuild_template',
    )
    parser.add_argument('makefile',
                        type=str,
                        help='Path to Rust makefile',
                        metavar='rust_makefile',
    )
    return parser

def main():
    args = build_args().parse_args()

    # Extract the version information from the Rust makefile
    with open(args.makefile, "r") as f:
        rust_mk_contents = f.readlines()

    regex = re.compile(release_number_regex)

    version_number = None

    for line in rust_mk_contents:
        match = regex.match(line)
        if match:
            version_number = match.group("value")
            break

    datestring = date.today().strftime("%Y.%m.%d")

    version = version_number + "_" + datestring

    # Write the PKGBUILD to stdout
    with open(args.template, "r") as f:
        pkgbuild = f.read()

    pkgbuild = pkgbuild.replace("{VERSION}", version)
    sys.stdout.write(pkgbuild)

if __name__ == "__main__":
    main()

# vim: set tabstop=4 shiftwidth=4 expandtab smarttab:
