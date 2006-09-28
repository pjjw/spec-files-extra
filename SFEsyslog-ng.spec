#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Notes: 
# This spec file will only work if CC is gcc. Do it at the command line
# before invoking this spec file (as opposed to putting it in %build below).
# That way the macros in Solaris.inc will know you've set it.
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

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

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
%{_datadir}/*

%changelog
* 
* Wed Sep 27 2006 - Eric Boutilier
- Initial spec
