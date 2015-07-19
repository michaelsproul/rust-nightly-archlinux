This code used to generate PKGBUILDs for a Rust Nightly package in the AUR, but I've passed maintenance over to someone else and they're no longer using this code. Original README below:

Rust & Cargo Nightly
====================

PKGBUILD generator for Arch Linux that makes installing the nightly Rust & Cargo builds easy.

This code is run every 24 hours (at 02:30 UTC) and updates the following AUR package:

https://aur.archlinux.org/packages/rust-nightly-bin/

## Components

The AUR package includes the following resources:

* The Rust compiler, `rustc`.
* Cargo, the Rust package manager.
* Offline HTML documentation, available at `/usr/local/share/doc/rust/html/index.html`
* A `.rs` MIME type for Rust source code.

## Syntax Highlighting

* [Emacs](https://github.com/rust-lang/rust/tree/master/src/etc/emacs)
* Vim: [Vundle/Pathogen](https://github.com/wting/rust.vim) or [AUR](https://aur.archlinux.org/packages/vim-rust-git/)
* [Gedit](https://aur.archlinux.org/packages/gedit-rust/)
* [Kate](https://aur.archlinux.org/packages/kate-syntax-rust-git/)

If you'd like to make changes, send me a pull request.
