#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define kde_version 3.5.8

Name:                SFEkdelibs3
Summary:             Base KDE3 libraries
Version:             %{kde_version}
Source:              http://files.kde.org/stable/%{kde_version}/src/kdelibs-%{version}.tar.bz2

Patch1:              kdelibs-01-doxygen.diff
Patch2:              kdelibs-02-libart.diff
Patch3:              kdelibs-03-makefile.diff
Patch4:              kdelibs-04-kmenuapps.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEgawk
Requires: SFEqt3
BuildRequires: SFEqt3-devel
Requires: SFEarts
BuildRequires: SFEarts-devel
Requires: SFElibidn
BuildRequires: SFElibidn-devel
Requires: SUNWzlib
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
Requires: SUNWgccruntime
Requires: SUNWxwplt
# The above bring in many things, including SUNWxwice and SUNWzlib
Requires: SUNWxwxft
# The above also pulls in SUNWfreetype2
BuildRequires: SFEdoxygen
Requires: SUNWgnu-coreutils
Requires: SFEcups
BuildRequires: SFEcups-devel
Requires: SUNWbzip
Requires: SUNWlxml
BuildRequires: SUNWlxml-devel
Requires: SUNWlxsl
BuildRequires: SUNWlxsl-devel
Requires: SUNWTiff
BuildRequires: SUNWTiff-devel
BuildRequires: SUNWgnome-common-devel
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEfam
BuildRequires: SFEfam-devel
Requires: SUNWopenssl-libraries
BuildRequires: SUNWopenssl-include
Requires: SUNWopensslr
Requires: SUNWkrbu
Requires: SUNWpcre
Requires: SUNWaspell
BuildRequires: SUNWaspell-devel
Requires: SFEopenexr
BuildRequires: SFEopenexr-devel

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n kdelibs-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

if [ "x`basename $CC`" != xgcc ]
then
	%error This spec file requires Gcc, set the CC and CXX env variables
fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/X11/include -I/usr/gnu/include -I/usr/sfw/include -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -I/usr/X11/include -I/usr/gnu/include -I/usr/sfw/include -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -lc -lsocket -lnsl `/usr/bin/libart2-config --libs`"

./configure -prefix %{_prefix} \
           --includedir %{_includedir}/kde3 \
           --datadir %{_datadir}/kde3 \
           --sysconfdir %{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --enable-final \
           --with-ssl-dir=/usr/sfw \
           --with-extra-includes="/usr/X11/include:/usr/gnu/include:/usr/sfw/include:/usr/include/pcre" \
           --with-gssapi=no


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# KDE requires the .la files
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

# Rename to avoid conflict with Gnome's applications.menu
mv ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/menus/applications.menu \
   ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/menus/kapplications.menu

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.la*
%dir %attr (0755, root, other) %{_libdir}/kde3
%{_libdir}/kde3/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/kde3
%dir %attr (0755, root, other) %{_datadir}/kde3/locale
%{_datadir}/kde3/locale/*
%dir %attr (0755, root, other) %{_datadir}/kde3/applications
%{_datadir}/kde3/applications/*
%dir %attr (0755, root, other) %{_datadir}/kde3/icons
%{_datadir}/kde3/icons/*
%dir %attr (0755, root, other) %{_datadir}/kde3/apps
%{_datadir}/kde3/apps/*
%dir %attr (0755, root, other) %{_datadir}/kde3/config
%{_datadir}/kde3/config/*
%dir %attr (0755, root, other) %{_datadir}/kde3/services
%{_datadir}/kde3/services/*
%dir %attr (0755, root, other) %{_datadir}/kde3/servicetypes
%{_datadir}/kde3/servicetypes/*
%dir %attr (0755, root, other) %{_datadir}/kde3/mimelnk
%{_datadir}/kde3/mimelnk/*
%dir %attr (0755, root, other) %{_datadir}/kde3/emoticons
%{_datadir}/kde3/emoticons/*
%dir %attr (0755, root, other) %{_datadir}/kde3/autostart
%{_datadir}/kde3/autostart/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/kde3
%{_includedir}/kde3/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/kde3
%dir %attr (0755, root, other) %{_datadir}/kde3/doc
%{_datadir}/kde3/doc/*

%changelog
* Tue Jan 12 2008 - moinak.ghosh@sun.com
- Initial spec.
