#
# spec file for package SFEuim
#
# includes module(s): uim
#
%include Solaris.inc

%define	src_name uim
%define	src_url	http://uim.googlecode.com/files

Name:		SFEuim
Summary:	UIM Input Method Framework
SUNW_BaseDir:            %{_basedir}
Version: 	1.4.1
Release:	1
License: 	LGPL
Group: 		System/GUI/GNOME
Source: 	%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		uim-01-ss11-patch.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-panel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-panel-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-base-libs

%package m17n
Summary:                 %{summary} - m17n
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEm17n-lib
Requires: SFEm17n-db
Requires: SUNWgnome-base-libs
Requires: SFEuim

%package anthy
Summary:                 %{summary} - anthy
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFElibanthy
Requires: SUNWgnome-base-libs
Requires: SFEuim

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
autoconf
automake
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -R/usr/openwin/lib -L/usr/openwin/lib -lX11"
./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --mandir=%{_mandir}			\
            --sysconfdir=%{_sysconfdir}         \
	    --enable-shared			\
	    --disable-static			\
            --disable-debug
make

%install
rm -rf ${RPM_BUILD_ROOT}
DESTDIR=${RPM_BUILD_ROOT} make install
find ${RPM_BUILD_ROOT} -name "*.a" -exec rm  {} \; -print
find ${RPM_BUILD_ROOT} -name "*.la" -exec rm {} \; -print

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%post
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules

%postun
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules

%clean
rm -rf ${RPM_BUILD_ROOT}

%files 
%defattr(-, root, bin)
%{_bindir}/*
%{_libdir}/lib*.so*
%{_libdir}/uim/plugin/libuim-skk.so
%{_libdir}/uim/plugin/libuim-custom-enabler.so
%{_libdir}/gtk-2.0/*
%{_libdir}/bonobo/*
%{_libexecdir}/uim-candwin-gtk
%{_libexecdir}/uim-helper-server
%{_libexecdir}/uim-toolbar-applet
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/man/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, root) %{_datadir}/emacs
%dir %attr (0755, root, root) %{_datadir}/emacs/site-lisp
%{_datadir}/emacs/site-lisp/*

%{_datadir}/uim/plugin.scm
%{_datadir}/uim/im.scm
%{_datadir}/uim/im-custom.scm
%{_datadir}/uim/lazy-load.scm
%{_datadir}/uim/init.scm
%{_datadir}/uim/im-switcher.scm
%{_datadir}/uim/default.scm
%{_datadir}/uim/util.scm
%{_datadir}/uim/key.scm
%{_datadir}/uim/ustr.scm
%{_datadir}/uim/action.scm
%{_datadir}/uim/load-action.scm
%{_datadir}/uim/i18n.scm
%{_datadir}/uim/uim-sh.scm
%{_datadir}/uim/uim-db.scm
%{_datadir}/uim/custom.scm
%{_datadir}/uim/custom-rt.scm
%{_datadir}/uim/direct.scm
%{_datadir}/uim/rk.scm
%{_datadir}/uim/generic.scm
%{_datadir}/uim/generic-custom.scm
%{_datadir}/uim/generic-key-custom.scm
%{_datadir}/uim/pyload.scm
%{_datadir}/uim/py.scm
%{_datadir}/uim/pyunihan.scm
%{_datadir}/uim/pinyin-big5.scm
%{_datadir}/uim/japanese.scm
%{_datadir}/uim/japanese-azik.scm
%{_datadir}/uim/japanese-kana.scm
%{_datadir}/uim/canna.scm
%{_datadir}/uim/canna-custom.scm
%{_datadir}/uim/canna-key-custom.scm
%{_datadir}/uim/prime.scm
%{_datadir}/uim/prime-custom.scm
%{_datadir}/uim/prime-key-custom.scm
%{_datadir}/uim/mana.scm
%{_datadir}/uim/mana-custom.scm
%{_datadir}/uim/mana-key-custom.scm
%{_datadir}/uim/tcode.scm
%{_datadir}/uim/trycode.scm
%{_datadir}/uim/tutcode.scm
%{_datadir}/uim/tutcode-key-custom.scm
%{_datadir}/uim/hangul.scm
%{_datadir}/uim/hangul2.scm
%{_datadir}/uim/hangul3.scm
%{_datadir}/uim/romaja.scm
%{_datadir}/uim/byeoru.scm
%{_datadir}/uim/byeoru-dic.scm
%{_datadir}/uim/byeoru-symbols.scm
%{_datadir}/uim/byeoru-custom.scm
%{_datadir}/uim/byeoru-key-custom.scm
%{_datadir}/uim/viqr.scm
%{_datadir}/uim/ipa-x-sampa.scm
%{_datadir}/uim/latin.scm
%{_datadir}/uim/spellcheck.scm
%{_datadir}/uim/spellcheck-custom.scm
%{_datadir}/uim/zaurus.scm
%{_datadir}/uim/scim.scm
%{_datadir}/uim/uim-module-manager.scm
%{_datadir}/uim/installed-modules.scm
%{_datadir}/uim/loader.scm
%{_datadir}/uim/skk.scm
%{_datadir}/uim/skk-editor.scm
%{_datadir}/uim/skk-custom.scm
%{_datadir}/uim/skk-key-custom.scm
%{_datadir}/uim/skk-dialog.scm

%{_datadir}/uim/pixmaps/unknown.svg
%{_datadir}/uim/pixmaps/direct.svg
%{_datadir}/uim/pixmaps/tcode.svg
%{_datadir}/uim/pixmaps/tutcode.svg
%{_datadir}/uim/pixmaps/byeoru.svg
%{_datadir}/uim/pixmaps/direct_input.svg
%{_datadir}/uim/pixmaps/on.svg
%{_datadir}/uim/pixmaps/off.svg
%{_datadir}/uim/pixmaps/ja_direct.svg
%{_datadir}/uim/pixmaps/ja_hiragana.svg
%{_datadir}/uim/pixmaps/ja_katakana.svg
%{_datadir}/uim/pixmaps/ja_halfkana.svg
%{_datadir}/uim/pixmaps/ja_halfwidth_alnum.svg
%{_datadir}/uim/pixmaps/ja_fullwidth_alnum.svg
%{_datadir}/uim/pixmaps/prime_mode_application.svg
%{_datadir}/uim/pixmaps/ko_direct.svg
%{_datadir}/uim/pixmaps/ko_hangulchar.svg
%{_datadir}/uim/pixmaps/ko_hangulword.svg
%{_datadir}/uim/pixmaps/ja_romaji.svg
%{_datadir}/uim/pixmaps/ja_kana.svg
%{_datadir}/uim/pixmaps/ja_azik.svg
%{_datadir}/uim/pixmaps/ja_nicola.svg
%{_datadir}/uim/pixmaps/ja_pocketbell.svg
%{_datadir}/uim/pixmaps/im_switcher.svg
%{_datadir}/uim/pixmaps/uim-dict.svg
%{_datadir}/uim/pixmaps/im_subst.svg
%{_datadir}/uim/pixmaps/py.svg
%{_datadir}/uim/pixmaps/pyunihan.svg
%{_datadir}/uim/pixmaps/pinyin-big5.svg
%{_datadir}/uim/pixmaps/mana.svg
%{_datadir}/uim/pixmaps/hangul2.svg
%{_datadir}/uim/pixmaps/hangul3.svg
%{_datadir}/uim/pixmaps/romaja.svg
%{_datadir}/uim/pixmaps/viqr.svg
%{_datadir}/uim/pixmaps/ipa-x-sampa.svg
%{_datadir}/uim/pixmaps/latin.svg
%{_datadir}/uim/pixmaps/scim.svg
%{_datadir}/uim/pixmaps/trycode.svg
%{_datadir}/uim/pixmaps/null.png
%{_datadir}/uim/pixmaps/uim-icon64.png
%{_datadir}/uim/pixmaps/uim-icon48.png
%{_datadir}/uim/pixmaps/uim-gray.png
%{_datadir}/uim/pixmaps/unknown.png
%{_datadir}/uim/pixmaps/direct.png
%{_datadir}/uim/pixmaps/tcode.png
%{_datadir}/uim/pixmaps/tutcode.png
%{_datadir}/uim/pixmaps/trycode.png
%{_datadir}/uim/pixmaps/byeoru.png
%{_datadir}/uim/pixmaps/direct_input.png
%{_datadir}/uim/pixmaps/on.png
%{_datadir}/uim/pixmaps/off.png
%{_datadir}/uim/pixmaps/ja_direct.png
%{_datadir}/uim/pixmaps/ja_hiragana.png
%{_datadir}/uim/pixmaps/ja_katakana.png
%{_datadir}/uim/pixmaps/ja_halfkana.png
%{_datadir}/uim/pixmaps/ja_halfwidth_alnum.png
%{_datadir}/uim/pixmaps/ja_fullwidth_alnum.png
%{_datadir}/uim/pixmaps/prime_mode_application.png
%{_datadir}/uim/pixmaps/ko_direct.png
%{_datadir}/uim/pixmaps/ko_hangulchar.png
%{_datadir}/uim/pixmaps/ko_hangulword.png
%{_datadir}/uim/pixmaps/ja_romaji.png
%{_datadir}/uim/pixmaps/py.png
%{_datadir}/uim/pixmaps/ja_kana.png
%{_datadir}/uim/pixmaps/ja_azik.png
%{_datadir}/uim/pixmaps/ja_nicola.png
%{_datadir}/uim/pixmaps/ja_pocketbell.png
%{_datadir}/uim/pixmaps/im_switcher.png
%{_datadir}/uim/pixmaps/uim-dict.png
%{_datadir}/uim/pixmaps/pyunihan.png
%{_datadir}/uim/pixmaps/pinyin-big5.png
%{_datadir}/uim/pixmaps/mana.png
%{_datadir}/uim/pixmaps/hangul2.png
%{_datadir}/uim/pixmaps/hangul3.png
%{_datadir}/uim/pixmaps/romaja.png
%{_datadir}/uim/pixmaps/viqr.png
%{_datadir}/uim/pixmaps/ipa-x-sampa.png
%{_datadir}/uim/pixmaps/latin.png
%{_datadir}/uim/pixmaps/scim.png
%{_datadir}/uim/pixmaps/canna.png
%{_datadir}/uim/pixmaps/prime.png
%{_datadir}/uim/pixmaps/uim-icon.png
%{_datadir}/uim/pixmaps/skk.svg
%{_datadir}/uim/pixmaps/skk.png

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files m17n
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_libdir}/uim/plugin/libuim-m17nlib.so
%{_datadir}/uim/m17nlib.scm
%{_datadir}/uim/pixmaps/m17n*

%files anthy
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_libdir}/uim/plugin/libuim-anthy.so
%{_datadir}/uim/anthy.scm
%{_datadir}/uim/anthy-custom.scm
%{_datadir}/uim/anthy-key-custom.scm
%{_datadir}/uim/pixmaps/anthy.png

%changelog
* Thu Jul 26 2007 - dougs@truemail.co.th
- Initial spec, borrowed from opensolaris input-method project
