#!/usr/bin/env python3

import re
import os
import sys
import argparse
import datetime

from sys import stderr
from datetime import date

release_number_regex = r"CFG_RELEASE_NUM[ ]*=[ ]*(?P<value>.*)"
release_label_regex = r"CFG_RELEASE_LABEL[ ]*=[ ]*(?P<value>.*)"

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

    r1 = re.compile(release_number_regex)
    r2 = re.compile(release_label_regex)

    version_number = None
    version_label = None

    for line in rust_mk_contents:
        if version_number is not None and version_label is not None:
            break

        m1 = r1.match(line)
        if m1:
            version_number = m1.group("value")
            continue

        m2 = r2.match(line)
        if m2:
            version_label = m2.group("value").replace("-", "_")

    datestring = date.today().strftime("%Y.%m.%d")

    version = version_number + version_label + "_" + datestring

    # Write the PKGBUILD to stdout
    with open(args.template, "r") as f:
        pkgbuild = f.read()

    pkgbuild = pkgbuild.replace("{VERSION}", version)
    sys.stdout.write(pkgbuild)

if __name__ == "__main__":
    main()

# vim: set tabstop=4 shiftwidth=4 expandtab smarttab:
