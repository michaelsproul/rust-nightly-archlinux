rust_makefile=https://raw.githubusercontent.com/mozilla/rust/master/mk/main.mk

default: rust-src-pkg

# Upload
upload: rust-upload

%-upload: %-src-pkg
	burp $*-nightly-bin-*.src.tar.gz

# Binary packages
%-bin-pkg: %.pkgbuild
	makepkg -p $<
	rm -rf pkg src

# Source packages
%-src-pkg: %.pkgbuild
	mkaurball -p $< -f
	@rm -f $*.xml

# PKGBUILDs
%.pkgbuild: temp/%_makefile.mk
	./make_pkgbuild.py templates/$*.pkgbuild $< > $@
	rm $<

# Version Makefiles
temp/%_makefile.mk: | temp
	curl $($*_makefile) -o $@

temp:
	mkdir -p $@

# Cleaning
clean:
	rm -rf pkg src
	rm -rf temp
	rm -rf rust.xml
	rm -f *.pkgbuild
	rm -f *.src.tar.gz
	rm -f *.pkg.tar.xz

super-clean: clean
	rm -f *.tar.gz
