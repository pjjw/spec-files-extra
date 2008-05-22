#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEconserver
Summary:             Serial console server + client
Version:             8.1.16
Source:              http://www.conserver.com/conserver-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n conserver-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%{_ldflags} -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --sysconfdir=%{_sysconfdir} \
            --with-uds \
            --with-libwrap \
            --with-openssl \
            --with-pam

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/conserver
%{_libdir}/conserver/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/examples
%dir %attr (0755, root, sys) %{_datadir}/examples/conserver
%{_datadir}/examples/conserver/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*.5
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*.8

%changelog
* Thu May 22 2008 - river@wikimedia.org
- Initial spec
