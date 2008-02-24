#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# The default build/install (and this spec files) doesn't install
# the required /etc/syslog-ng/syslog-ng.conf.solaris file; instead
# a sample one for solaris comes with the source in the doc directory.
# It's called syslog-ng.conf.solaris.

%include Solaris.inc

Name:                SFEeventlog
Summary:             Library needed by Syslog-ng
Version:             0.2.7
Source:              http://www.balabit.com/downloads/files/syslog-ng/sources/stable/src/eventlog-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n eventlog-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# This source is gcc-centric, therefore...
export CC=/usr/sfw/bin/gcc
# export CFLAGS="%optflags"
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"

export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --sysconfdir=%{_sysconfdir} \
            --enable-full-dynamic \
            --mandir=%{_mandir}

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Feb 24 2008 - Moinak Ghosh
- Initial spec
- Initial spec. This is needed by SFEsyslog-ng.
