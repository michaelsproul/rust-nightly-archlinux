RUST_MAKEFILE=https://raw.githubusercontent.com/mozilla/rust/master/mk/main.mk

.PHONY: default PKGBUILD clean

default: PKGBUILD

upload: package
	burp rust-nightly-bin-*.tar.gz

package: PKGBUILD
	makepkg --source

PKGBUILD: rust_makefile.mk
	./make_pkgbuild.py PKGBUILD.template VERSION rust_makefile.mk > PKGBUILD
	rm rust_makefile.mk
	updpkgsums

rust_makefile.mk:
	curl $(RUST_MAKEFILE) -o rust_makefile.mk

clean:
	rm -f rust_makefile.mk PKGBUILD
	rm -rf src pkg
	rm -f rust-nightly-bin-*.tar.gz
	rm -f rust-nightly-bin-*.tar.xz

superclean: clean
	rm -r rust-nightly-*.tar.gz
