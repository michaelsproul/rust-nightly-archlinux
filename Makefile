RUST_MAKEFILE=https://raw.githubusercontent.com/mozilla/rust/master/mk/main.mk

.PHONY: default upload package PKGBUILD clean superclean

default: PKGBUILD

upload: package
	burp rust-nightly-bin-*.tar.gz

package: PKGBUILD
	mkaurball

PKGBUILD: rust_makefile.mk
	./make_pkgbuild.py PKGBUILD.template rust_makefile.mk > PKGBUILD
	rm rust_makefile.mk

rust_makefile.mk:
	curl $(RUST_MAKEFILE) -o rust_makefile.mk

clean:
	rm -f rust_makefile.mk PKGBUILD
	rm -rf src pkg
	rm -f rust-nightly-bin-*.tar.gz
	rm -f rust-nightly-bin-*.tar.xz

superclean: clean
	rm -f rust-nightly-*.tar.gz
