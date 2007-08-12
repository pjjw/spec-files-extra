#
# spec file for package libvorbis (Version 1.0)
#
# Copyright (c) 2003 SuSE Linux AG, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://www.suse.de/feedback/
#
# Owner: yippi
#
# neededforbuild  libogg libogg-devel
# usedforbuild    aaa_base acl attr bash bind9-utils bison coreutils cpio cpp cvs cyrus-sasl2 db devs diffutils e2fsprogs file filesystem fillup findutils flex gawk gdbm-devel glibc glibc-devel glibc-locale gpm grep groff gzip info insserv kbd less libacl libattr libgcc libstdc++ libxcrypt m4 make man mktemp modutils ncurses ncurses-devel net-tools netcfg pam pam-devel pam-modules patch permissions ps rcs readline sed sendmail shadow strace syslogd sysvinit tar texinfo timezone unzip util-linux vim zlib zlib-devel autoconf automake binutils bzip2 cracklib gcc gdbm gettext libogg libogg-devel libtool perl rpm

Name:         libvorbis
Summary:      The Vorbis General Audio Compression Codec
Version:      1.2.0
Release:      95
Group:        System/Libraries
License:      BSD
URL:          http://downloads.xiph.org/
Source:       http://downloads.xiph.org/releases/vorbis/%{name}-%{version}.tar.gz
Source1:       l10n-configure.sh
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
Ogg Vorbis is a fully open, non-proprietary, patent-and-royalty-free,
and general-purpose compressed audio format for audio and music at fixed
and variable bitrates from 16 to 128 kbps/channel.

Authors:
--------
    Monty <monty@xiph.org>
    Xiphophorus Company <team@xiph.org>

%package devel
Summary:      Development package for libvorbis
Group:        Development/Libraries/C and C++
Requires:     libogg-devel
Requires:     %{name} = %{version}

%description devel
This package contains the header files and documentation
needed to develop applications with libvorbis.

Authors:
--------
    Monty <monty@xiph.org>
    Xiphophorus Company <team@xiph.org>

%prep
%setup

bash -x %SOURCE1

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export LDFLAGS="%_ldflags"

aclocal $ACLOCAL_FLAGS
autoconf
automake -a -f
#autoreconf --force --install
./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
	    --with-ogg-libraries=%{_libdir}	\
	    --enable-shared			\
	    --disable-shared
make

%install
make DESTDIR=$RPM_BUILD_ROOT docdir=%{_datadir}/gtk-doc/html/%{name}-devel install
# create an old compatible m4 file
sed -e s/XIPH_PATH_VORBIS/AM_PATH_VORBIS/g < $RPM_BUILD_ROOT%{_datadir}/aclocal/vorbis.m4 > $RPM_BUILD_ROOT%{_datadir}/aclocal/vorbis-old.m4

%post
%run_ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING AUTHORS README HACKING
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/vorbis
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_datadir}/aclocal/*.m4
%{_datadir}/gtk-doc

%changelog -n libvorbis
* Sun Aug 12 2007 - dougs@truemail.co.th
- copied from spec-files to provide 64bit libraries
* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 1.2.0.
* Tue Dec 27 2005 - damien.carbery@sun.com
- Bump to 1.1.2
* Tue Sep 20 2005 - brian.cameron@sun.com
- Bump to 1.1.1
* Mon Jun 06 2005 - brian.cameron@sun.com
- Removed libvorbis-01-configure.diff since it is no longer
  necessary.
* Wed Aug 25 2004 - brian.cameron@sun.com
- Moved gtk-docs to %{_datadir}/gtk-doc
* Sat Mar 01 2003 - adrian@suse.de
- let libvorbis-devel require libogg-devel
* Fri Jan 17 2003 - tiwai@suse.de
- fixed m4 macro (bug #21267).
* Thu Jan 09 2003 - kukuk@suse.de
- Add *.la files to -devel filelist
* Wed Dec 04 2002 - tiwai@suse.de
- fixed the undefined weak links.
- renamed m4.dif and lib64.dif with libvorbis- prefix to avoid
  filename conflictions.
* Thu Sep 19 2002 - tiwai@suse.de
- don't add -I/usr/include to VORBIS_VFLAGS.
- fix test for prefix.
- move devel documents under %%{_docdir}/libvorbis-devel.
* Mon Aug 12 2002 - tiwai@suse.de
- added Requires %%{name} = %%{version} to devel package.
* Tue Jul 23 2002 - tiwai@suse.de
- fixed m4 file for lib64.
- provides the backward compatible m4 file.
* Mon Jul 22 2002 - tiwai@suse.de
- updated to version 1.0.
- clean up the spec file.
- added %%run_ldconfig.
* Wed Jun 12 2002 - meissner@suse.de
- rm acinclude.m4 so we don't have the problematic ogg.m4 (which contains
  /lib hardcoded).
* Thu Apr 18 2002 - kukuk@suse.de
- Remove additional optimization, default is better
- Add --libdir to configure to build on x86_64
* Thu Feb 07 2002 - tiwai@suse.de
- fixed build on s390x.
* Fri Jan 04 2002 - tiwai@suse.de
- updated to RC3.
  sync with cvs 2002.01.04.
* Tue Dec 04 2001 - tiwai@suse.de
- sync with cvs 2001.12.04.
* Wed Oct 24 2001 - tiwai@suse.de
- sync with cvs 20011024.
  + fixed/updated documents
  + tuned up parameters
  + bugfixes on 64bit arch.
- removed Requires to libogg.
* Sat Oct 20 2001 - schwab@suse.de
- Fix use of qsort.
* Mon Aug 13 2001 - tiwai@suse.de
- updated to 1.0rc2 from cvs 20010813.
* Thu Jun 07 2001 - tiwai@suse.de
- fixed build with the recent libtool.
* Tue Apr 03 2001 - bk@suse.de
- make use of RPM_OPT_FLAGS
- include the include/vorbis dir into the file list(+rpm-macroized)
* Mon Mar 12 2001 - tiwai@suse.de
- corrected copyright in spec file.
* Mon Feb 26 2001 - tiwai@suse.de
- Updated to 1.0beta4.
* Wed Jan 31 2001 - tiwai@suse.de
- Initial version: 1.0beta3.
