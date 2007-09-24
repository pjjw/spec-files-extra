#
# spec file for package SFEpython-pyrtf
#
# includes module(s): PyRTF
#
%define src_name PyRTF
%define src_url  http://dl.sourceforge.net/sourceforge/pyrtf

%define python_version 2.4

%include Solaris.inc

Name:                SFEpython-pyrtf
Summary:             Rich Text Format (RTF) document generation for Python
Version:             0.45
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Mon Sep 24 2007 - trisk@acm.jhu.edu 
- Initial spec
