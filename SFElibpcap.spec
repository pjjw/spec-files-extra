#
#
# !! Note:
# Must use GNU ld. This is a bit tricky because it's
# called gld on OpenSolaris and lives in /usr/sfw/bin,
# and setting LD=/usr/sfw/bin/gld doesn't work because
# this source's configure ignores $LD. What I did was 
# symlink'd gld to ld and made sure it was found in $PATH 
# ahead of /usr/ccs/bin/ld.
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

%prep
%setup -q -n libpcap-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

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
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* 
* Fri Sep 29 2006 - Eric Boutilier
- Wrestled with it to get it to build shared, not static, lib. (I won :) )
-
* Fri Sep 01 2006 - Eric Boutilier
- Initial spec
