#
# spec file for package SFEbzr
#
# includes module(s): bzr
#
%include Solaris.inc

%define python_version 2.4

Name:			SFEbzr
Summary:		Bazaar Source Code Management System
License:		GPL
Group:			system/dscm
Version:		0.6.2
Release:		1
Distribution:		spec-files-extra
Vendor:			http://pkgbuild.sf.net/spec-files-extra
Source:			http://www.bazaar-ng.org/pkg/bzr-%{version}.tar.gz
URL:			http://www.bazaar-ng.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWPython
Requires: SUNWcsu
BuildRequires: SUNWPython-devel


%description
Bazaar source code management system.

%prep
%setup -q -n bzr-%{version}

%build
export PYTHON="/usr/bin/python"
CFLAGS="$RPM_OPT_FLAGS"
python setup.py build

%install
python setup.py install --prefix=$RPM_BUILD_ROOT%{_prefix}
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages

# Delete precompiled py code (*.pyc). May not be compatibile with dest system.
find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.pyc" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*

%changelog
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEbzr
- change to root:bin to follow other JDS pkgs.
* Sat Jan 7 2006  <glynn.foster@sun.com>
- initial version
