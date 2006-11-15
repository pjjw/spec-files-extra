#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

# Proftpd needs to install in a special place to avoid name collisions with
# ftpshut, ftpcount, and ftpwho. Putting it in /usr/gnu is an option; but
# because its a server app -- as with SUNWapchu (Apache) -- putting it under
# /usr/<appname> seems to make more sense. Therefore...

%define _prefix %{_basedir}/proftpd

Name:                SFEproftpd
Summary:             Highly configurable FTP server
Version:             1.3.0
Source:              ftp://ftp.proftpd.org/distrib/source/proftpd-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: %name-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n proftpd-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

export install_user=$LOGNAME
export install_group=other

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rmdir ${RPM_BUILD_ROOT}%{_prefix}/libexec
rmdir ${RPM_BUILD_ROOT}%{_prefix}/var/proftpd
rmdir ${RPM_BUILD_ROOT}%{_prefix}/var

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man?
%{_mandir}/man?/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/proftpd.conf

%changelog
* 
* Tue Nov 14 2006 - Eric Boutilier
- Initial spec
