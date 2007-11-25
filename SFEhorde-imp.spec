#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEhorde-imp
Summary:             Horde IMP Webmail
Version:             4.1.4-rc1
Source:              http://ftp.horde.org/pub/imp/imp-h3-%{version}.tar.gz

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEphp
Requires: SFEhorde

%prep
%setup -q -n imp-h3-%version

#%build

#dummy - noting to make

%install
rm -rf $RPM_BUILD_ROOT

#make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/horde/imp
cp -pr * $RPM_BUILD_ROOT/var/horde/imp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, webservd, webservd) %{_localstatedir}/horde/imp/*
%{_localstatedir}/horde/imp/*


%changelog
* 
* Sun Mar 11 2007 - Thomas Wagner
- Initial spec
