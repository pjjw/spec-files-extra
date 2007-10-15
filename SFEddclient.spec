#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEddclient
Summary:             update dynamic DNS entries for accounts on dynamic DNS providers
Version:             3.7.0
Source:              http://%{sf_mirror}/sourceforge/ddclient/ddclient-%{version}.tar.bz2

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n ddclient-%version

%build

# Written in perl; nothing to build
exit 0

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/etc/ddclient
cp ddclient $RPM_BUILD_ROOT/usr/sbin/
cp sample-etc_ddclient.conf $RPM_BUILD_ROOT/etc/ddclient/ddclient.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%attr(0600, root, sys) %{_sysconfdir}/ddclient/ddclient.conf

%changelog
* 
* Sat Sep 30 2006 - Eric Boutilier
- Initial spec
