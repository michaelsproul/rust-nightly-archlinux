aur_repo=ssh://aur@aur4.archlinux.org/rust-nightly-bin.git
rust_makefile=https://raw.githubusercontent.com/mozilla/rust/master/mk/main.mk

default: PKGBUILD

upload: PKGBUILD | aur-repo
	cd aur-repo && \
	git pull && \
	cp ../PKGBUILD ../rust-nightly.conf ../rust.install . && \
	mksrcinfo && \
	git commit -a -m "Update: $(shell date --utc)" || echo "Nothing to commit, that's fine."
	cd aur-repo && git push origin master

PKGBUILD: templates/rust.pkgbuild temp/rust_makefile.mk
	./make_pkgbuild.py $^ > $@
	rm temp/rust_makefile.mk # remove makefile so it updates next time.

temp/rust_makefile.mk: | temp
	curl $(rust_makefile) -o $@

aur-repo:
	git clone $(aur_repo) $@

temp:
	mkdir -p temp

# Cleaning
clean:
	rm -rf pkg src
	rm -rf temp
	rm -f PKGBUILD
	rm -f *.src.tar.gz
	rm -f *.pkg.tar.xz

super-clean: clean
	rm -f *.tar.gz
