#!/usr/bin/env python3

import re
import os
import sys

from sys import stderr

usage = "Usage: make_pkgbuild.py <template> <version file> <rust makfile>"
release_number_regex = r"CFG_RELEASE_NUM[ ]*=[ ]*(?P<value>.*)"
release_label_regex = r"CFG_RELEASE_LABEL[ ]*=[ ]*(?P<value>.*)"

def read_version_file(version_file):
	if os.path.exists(version_file):
		with open(version_file, "r") as f:
			text = f.read()
		old_version = eval(text)
		return old_version
	else:
		return None


def main():
	if len(sys.argv) != 4:
		print(usage, file=stderr)
		sys.exit(1)

	template_file = sys.argv[1]
	version_file = sys.argv[2]
	rust_makefile = sys.argv[3]

	# Extract the version information
	with open(rust_makefile, "r") as f:
		text = f.readlines()

	r1 = re.compile(release_number_regex)
	r2 = re.compile(release_label_regex)

	version_number = None
	version_label = None

	for line in text:
		if version_number is not None and version_label is not None:
			break

		m1 = r1.match(line)
		if m1:
			version_number = m1.group("value")
			continue

		m2 = r2.match(line)
		if m2:
			version_label = m2.group("value").replace("-", "_")

	version = version_number + version_label + "_nightly"

	old_version = read_version_file(version_file)

	# Work out the release number
	if old_version is None or version != old_version["name"]:
		release_number = 1
	else:
		release_number = old_version["release"] + 1

	# Update the version file
	with open(version_file, "w") as f:
		output_ver = {"name": version, "release": release_number}
		f.write(repr(output_ver) + "\n")

	# Write the PKGBUILD to stdout
	with open(template_file, "r") as f:
		pkgbuild = f.read()

	pkgbuild = pkgbuild.replace("{VERSION}", version).replace("{RELEASE}", str(release_number))
	sys.stdout.write(pkgbuild)

if __name__ == "__main__":
	main()
