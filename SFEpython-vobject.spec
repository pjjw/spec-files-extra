#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%define src_name vobject
%define python_version 2.4

%include Solaris.inc

Name:                SFEpython-vobject
URL:                 http://vobject.skyhouseconsulting.com/
Summary:             vobject - a Python iCalendar library
Version:             0.4.9
Source:              http://vobject.skyhouseconsulting.com/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
BuildRequires: SFEpython-setuptools
Requires: SUNWPython

%prep
%setup -q -n %{src_name}-%version

%build
exit 0

%install
rm -rf $RPM_BUILD_ROOT
/usr/bin/python%{python_version} ./setup.py install --root=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Fri Feb 15 2008 - jijun.yu@sun.com 
- add a build dependency: SFEpython-setuptools
* Tue Dec 11 2007 - nonsea@users.sourceforge.net
- Initial spec
