#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEhorde
Summary:             Horde Framework
Version:             3.1.3
Source:              http://ftp.horde.org/pub/horde/horde-%{version}.tar.gz

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEphp

%prep
%setup -q -n horde-%version

#%build

#dummy - noting to make

%install
rm -rf $RPM_BUILD_ROOT

#make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/horde
cp -pr * $RPM_BUILD_ROOT/var/horde

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, webservd, webservd) %{_localstatedir}/horde/*
%{_localstatedir}/horde/*



%changelog
* 
* Sun Mar 11 2007 - Thomas Wagner
- Initial spec
