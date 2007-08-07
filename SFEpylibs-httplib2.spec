#
# spec file for package SFEpylibs-httplib
#
# includes module(s): httplib2
#

%define real_name httplib2
%define python_version 2.4

%include Solaris.inc
Name:                    SFEpylibs-httplib2
Summary:                 A comprehensive HTTP client library for Python.
URL:                     http://code.google.com/p/httplib2
Version:                 0.3.0
Source:                  http://httplib2.googlecode.com/files/%{real_name}-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SUNWPython

%prep
%setup -q -n %{real_name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --home=$RPM_BUILD_ROOT/%{_prefix}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python/* $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rm -rf $RPM_BUILD_ROOT%{_libdir}/python

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python?.?/vendor-packages

%changelog
* Tue Aug 07 2007 - jijun.yu@sun.com
- Bump to 0.3.0
- Modify the webpage and download link.

* Tue Nov 14 2006 - halton.huo@sun.com
- Initial spec file
