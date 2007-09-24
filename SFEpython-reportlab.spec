#
# spec file for package SFEpython-reportlab
#
# includes module(s): reportlab
#
%define src_name    ReportLab
%define src_version 2_1
%define src_url     http://www.reportlab.org/ftp/

%define python_version 2.4

%include Solaris.inc

Name:                SFEpython-reportlab
Summary:             ReportLab Toolkit - PDF library for Python
URL:                 http://www.reportlab.org/
Version:             2.1
Source:              %{src_url}/%{src_name}_%{src_version}.tgz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
Requires: SUNWPython

%prep
%setup -q -n reportlab_%{src_version}

%build
exit 0

%install
rm -rf $RPM_BUILD_ROOT
cd reportlab
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
