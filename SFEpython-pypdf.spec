#
# This package is named SFEpython-pypdf instead of just SFEpypdf
# because when a python (or perl or php) package delivers a library (as opposed
# to an application or commands) it seems to make more sense to include the
# language name in the package name.
#
%include Solaris.inc

%define python_version 2.4

Name:                SFEpython-pypdf
Summary:             PDF toolkit library for Python
Version:             1.9
Source:              http://pybrary.net/pyPdf/pyPdf-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
Requires: SUNWPython

%prep
%setup -q -n pyPdf-%version

%build
# Bypass build because the Python distutils (setup.py) standard specifies 
# that the install step (below) implicitly does a build anyway.
exit 0

%install
# The %prefix setting and any other build/install vars are set automatically.
# See /usr/lib/python2.4/config/Makefile. Thus, it is possible (in fact,
# preferred IMO) to not specify any here, except, of course, $RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT
/usr/bin/python%{python_version} setup.py install --root=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Mon Sep 24 2007 - trisk@acm.jhu.edu
- Move to vendor-packages
* Mon Apr 02 2007 - Eric Boutilier
- Initial spec
