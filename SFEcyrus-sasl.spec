#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc

Name:                SFEcyrus-sasl
Summary:             Simple Authentication and Security Layer library
Version:             2.1.22
Source:              ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/cyrus-sasl-%{version}.tar.gz
Patch1:              cyrus-sasl-01.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWsqlite3
BuildRequires: SUNWsqlite3
Requires: SUNWopenssl-libraries
BuildRequires: SUNWopenssl-include
Requires: SFElibntlm
BuildRequires: SFElibntlm-devel

%prep
%setup -q -n cyrus-sasl-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# needed to prevent an error during configure - strip whitespace
CFLAGS="%optflags -I/usr/gnu/include -I/usr/sfw/include"
export CFLAGS="`echo $CFLAGS`"
export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib"

./configure -prefix %{_prefix} \
           --enable-shared=yes \
           --enable-static=no \
           --with-dbpath=%{_sysconfdir}/sasldb2 \
           --with-plugindir=%{_libdir}/sasl2 \
           --sysconfdir %{_sysconfdir} \
           --mandir %{_mandir} \
           --with-ipctype=doors \
           --with-openssl=/usr/sfw

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/sasl2/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/sbin
%{_prefix}/sbin/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/sasl2
%{_libdir}/sasl2/lib*.so*
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/sasl
%{_includedir}/sasl/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%changelog
* Fri Oct 24 2008 - jedy.wang@sun.com
- Fixes plugindir problem.
* Fri Jun 06 2008 - river@wikimedia.org
- strip whitespace from $CFLAGS otherwise autoconf gets upset
* Sun Feb 03 2008 - moinak.ghosh@sun.com
- Add dependency on SFElibntlm.
* Tue Jan 15 2008 - moinak.ghosh@sun.com
- Initial spec.
