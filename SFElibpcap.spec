#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFElibpcap
Summary:             Packet Capture library 
Version:             0.9.4
Source:              http://www.tcpdump.org/release/libpcap-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libpcap-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

# Must use GNU ld, which is called gld on OpenSolaris and lives
# in /usr/sfw/bin. Setting LD=/usr/sfw/bin/gld doesn't work
# because this source's configure ignores $LD. So I've hacked
# Makefile.in on-the-fly thusly:

perl -i.orig -lpe 's/^\tld/\tgld/ if $. == 115' Makefile.in

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS
make -j$CPUS shared

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
make install-shared DESTDIR=$RPM_BUILD_ROOT

cd ${RPM_BUILD_ROOT}%{_libdir}
rm libpcap.a
ln -s libpcap.so.%version libpcap.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/pcap.3

%changelog
* Wed Oct 25 2006 - Eric Boutilier
- Added an on-the-fly patch to force it to use gld; also created devel subpkg
* Fri Sep 29 2006 - Eric Boutilier
- Wrestled with it to get it to build shared, not static, lib. (I won :) )
* Fri Sep 01 2006 - Eric Boutilier
- Initial spec
