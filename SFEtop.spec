#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEtop
License:             BSD Style
Summary:             Top is a Unix utility that provides a rolling display of top cpu using processes
Version:             3.7beta4
URL:                 http://www.unixtop.org/
Source:              %{sf_download}/unixtop/top-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWcsu

%prep
%setup -q -n top-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --enable-shared=yes \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
mv ${RPM_BUILD_ROOT}%{_prefix}/bin/i386 ${RPM_BUILD_ROOT}%{_prefix}/bin/i86

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/man
%{_datadir}/man/*

%changelog
* Fri Feb 08 2008 - moinak.ghosh@sun.com
- Initial spec.
