#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEarts
Summary:             Software to simulate a modular analog synthesizer
Version:             1.5.8
Source:              http://files.kde.org/stable/3.5.8/src/arts-%{version}.tar.bz2

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEqt3
BuildRequires: SFEqt3-devel
Requires: SUNWgnome-audio
BuildRequires: SUNWgnome-audio-devel
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWogg-vorbis
BuildRequires: SUNWogg-vorbis-devel
Requires: SFElibmad
BuildRequires: SFElibmad-devel
Requires: SFEjack
BuildRequires: SFEjack-devel
#Requires: SFEnas
BuildRequires: SFEnas-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n arts-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/X11/include -I/usr/gnu/include -I/usr/sfw/include"

export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib"

./configure -prefix %{_prefix} --enable-shared=yes --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/mcop
%{_libdir}/mcop/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/arts
%{_includedir}/arts/*
%dir %attr (0755, root, other) %{_includedir}/artsc
%{_includedir}/artsc/*

%changelog
* Fri Jan 11 2008 - moinak.ghosh@sun.com
- Initial spec.
