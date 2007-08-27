#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define  src_name cyrus-sasl

Name:                SFEsaslauthd
Summary:             SASL v2 authentication daemon
Version:             2.1.22
Source:              http://ftp.andrew.cmu.edu/pub/cyrus-mail/%{src_name}-%{version}.tar.gz
URL:                 http://asg.web.cmu.edu/sasl/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWopenssl-libraries
BuildRequires: SUNWlibsasl
BuildRequires: SUNWgss

%prep
%setup -q -n %{src_name}-%{version}

%build

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

autoconf
# configure, but don't build the library
./configure --prefix=%{_prefix}            \
            --bindir=%{_bindir}            \
            --sbindir=%{_sbindir}          \
            --libdir=%{_libdir}            \
            --sysconfdir=%{_sysconfdir}    \
            --mandir=%{_mandir}            \
            --with-plugindir=/usr/lib/sasl \
            --with-configdir=/etc/sasl     \
            --with-ipctype=doors           \
            --with-openssl=/usr/sfw        \
            --with-saslauthd=%{_localstatedir}/run/saslauthd

cd saslauthd

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

cd saslauthd

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%changelog 
* Mon Aug 27 2007 - trisk@acm.jhu.edu
- Initial version
