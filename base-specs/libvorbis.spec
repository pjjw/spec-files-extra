#
# spec file for package libogg (Version 1.0)
#
# Copyright (c) 2003 SuSE Linux AG, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://www.suse.de/feedback/
#
# Owner: yippi
#
# neededforbuild  
# usedforbuild    aaa_base acl attr bash bind9-utils bison coreutils cpio cpp cvs cyrus-sasl2 db devs diffutils e2fsprogs file filesystem fillup findutils flex gawk gdbm-devel glibc glibc-devel glibc-locale gpm grep groff gzip info insserv kbd less libacl libattr libgcc libstdc++ libxcrypt m4 make man mktemp modutils ncurses ncurses-devel net-tools netcfg pam pam-devel pam-modules patch permissions ps rcs readline sed sendmail shadow strace syslogd sysvinit tar texinfo timezone unzip util-linux vim zlib zlib-devel autoconf automake binutils bzip2 cracklib gcc gdbm gettext libtool perl rpm

Name:         libogg
Summary:      Ogg Bitstream Library
Version:      1.1.3
Release:      92
Group:        System/Libraries
License:      BSD
URL:          http://downloads.xiph.org/
Source:       http://downloads.xiph.org/releases/ogg/%{name}-%{version}.tar.gz
#Source1:       l10n-configure.sh
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
Libogg is a library for manipulating ogg bitstreams.  It handles
both making ogg bitstreams and getting packets from ogg bitstreams.

Authors:
--------
    Monty <monty@xiph.org>
    Xiphophorus Company <team@xiph.org>

%package devel
Summary:      Development package for libogg
Group:        Development/Libraries/C and C++
Requires:     %{name} = %{version}

%description devel
This package contains the header files and documentation
needed to develop applications with libogg.

Authors:
--------
    Monty <monty@xiph.org>
    Xiphophorus Company <team@xiph.org>

%prep
%setup

#bash -x %SOURCE1

%build

export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export LDFLAGS="%_ldflags"

autoreconf --force --install
./configure --prefix=%{_prefix}		\
	    --libdir=%{_libdir}		\
	    --includedir=%{_includedir}	\
	    --datadir=%{_datadir}	\
	    --enable-shared		\
	    --disable-static
make

%install
make DESTDIR=$RPM_BUILD_ROOT docdir=%{_datadir}/gtk-doc/html/%{name}-devel install
# create an old compatible m4 file
sed -e s/XIPH_PATH_OGG/AM_PATH_OGG/g < $RPM_BUILD_ROOT%{_datadir}/aclocal/ogg.m4 > $RPM_BUILD_ROOT%{_datadir}/aclocal/ogg-old.m4

%post
%run_ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES COPYING README
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/ogg
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_datadir}/aclocal/*.m4
%{_datadir}/gtk-doc

%changelog -n libogg
* Mon Oct  1 2007 - Thomas Wagner
- base-spec/libogg.spec vorbis.spec
  removed Source1 l10* and in %prep removed calling l10*
  since it's not needed or not there
* Sun Aug 12 2007 - dougs@truemail.co.th
- copied from spec-files to provide 64bit libraries
* Tue Dec 27 2005 - damien.carbery@sun.com
- Bump to 1.1.3.
* Mon Jun 06 2005 - brian.cameron@sun.com
- Fixed PKG_CONFIG_PATH so libogg-02-uninstalled-pc.diff is no longer
  necessary.  Removed libogg-01-configure.diff since it is no longer
  needed either.
* Wed Aug 25 2004 - brian.cameron@sun.com
- Moved gtk-docs to %{_datadir}/gtk-doc.
* Thu Jan 09 2003 - kukuk@suse.de
- Add *.la files to -devel filelist
* Thu Sep 19 2002 - tiwai@suse.de
- fixed the conflict between the last ogg.m4 fix and 64bit
  fix patches.
- moved devel documents under %%{_docdir}/libogg-devel.
* Tue Sep 17 2002 - pthomas@suse.de
- ogg.m4:
- If prefix is /usr, don't add -I$prefix/include to OGG_CFLAGS
  and don't add -L$prefix/lib to OGG_LIBS. While the latter is
  just unnecessary, the former can be dangerous and will make
  gcc warn.
- Fix test for prefix.
* Mon Aug 12 2002 - tiwai@suse.de
- added Requires %%{name} = %%{version} to devel package.
* Tue Jul 23 2002 - tiwai@suse.de
- provides the backward compatible m4 file.
* Mon Jul 22 2002 - tiwai@suse.de
- updated to version 1.0.
- clean up the spec file.
- added %%run_ldconfig.
* Mon Jun 10 2002 - adrian@suse.de
- fix ogg.m4 for lib64 systems
* Thu Apr 18 2002 - kukuk@suse.de
- Add --libdir to configure to compile on x86_64
* Thu Feb 07 2002 - tiwai@suse.de
- fixed compile on s390x.
* Fri Jan 04 2002 - tiwai@suse.de
- updated to RC3.
  sync with cvs 2002.01.04.
* Tue Dec 04 2001 - tiwai@suse.de
- sync with cvs 2001.12.04.
* Wed Oct 24 2001 - tiwai@suse.de
- sync with cvs 20011024.
  + fixed documents
- removed Requires to libogg from devel.
* Mon Aug 13 2001 - tiwai@suse.de
- updated to 1.0rc2 from cvs 20010813.
* Thu Jun 07 2001 - tiwai@suse.de
- fixed build with the recent libtool.
* Mon Mar 12 2001 - tiwai@suse.de
- corrected copyright in spec file.
* Mon Feb 26 2001 - tiwai@suse.de
- Updated to 1.0beta4.
* Wed Jan 31 2001 - tiwai@suse.de
- Initial version: 1.0beta3.
