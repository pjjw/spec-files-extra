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

Name:                SFEsyslog-ng
Summary:             Syslog-ng tries to fill the gaps original syslogd's were lacking
Version:             1.6.11
Source:              http://www.balabit.com/downloads/syslog-ng/1.6/src/syslog-ng-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n syslog-ng-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# This source is gcc-centric, therefore...
export CC=/usr/sfw/bin/gcc
# export CFLAGS="%optflags"
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointers"

export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --sysconfdir=%{_sysconfdir} \
            --enable-full-dynamic \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man5
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man5/syslog-ng.conf.5
%{_mandir}/man8/syslog-ng.8

%changelog
* Sun Nov 05 2006 - Eric Boutilier
- Force gcc
* Wed Sep 27 2006 - Eric Boutilier
- Initial spec
