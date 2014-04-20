#!/usr/bin/env python3

import re
import os
import sys
import datetime

from sys import stderr
from datetime import date

usage = "Usage: make_pkgbuild.py <pkgbuild template> <rust makefile>"
release_number_regex = r"CFG_RELEASE_NUM[ ]*=[ ]*(?P<value>.*)"
release_label_regex = r"CFG_RELEASE_LABEL[ ]*=[ ]*(?P<value>.*)"

def main():
	# Parse command-line args
	if len(sys.argv) != 3:
		print(usage, file=stderr)
		sys.exit(1)

	template_file = sys.argv[1]
	rust_makefile = sys.argv[2]

	# Extract the version information from the Rust makefile
	with open(rust_makefile, "r") as f:
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
	with open(template_file, "r") as f:
		pkgbuild = f.read()

	pkgbuild = pkgbuild.replace("{VERSION}", version)
	sys.stdout.write(pkgbuild)

if __name__ == "__main__":
	main()
