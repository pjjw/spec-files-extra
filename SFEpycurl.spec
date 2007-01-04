#
# spec file for package SFEpycurl
#
# includes module(s): pycurl
#
%include Solaris.inc

%define python_version 2.4

Name:			SFEpycurl
Summary:		Python interface to libcurl
License:		LGPL
Version:		7.15.5.1
Source:			http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz
Patch1:                 pycurl-01-source-opts.diff
URL:			http://pycurl.sourceforge.net/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWPython
%include default-depend.inc
Requires: SFEcurl
BuildRequires: SUNWPython-devel

%prep
%setup -q -n pycurl-%{version}
%patch1 -p1

%build
export PYTHON="/usr/bin/python"
export CFLAGS="$RPM_OPT_FLAGS -I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix=$RPM_BUILD_ROOT%{_prefix}
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages

# Delete optimized py code.
find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/pycurl

%changelog
* Wed Jan  3 2007 - laca@sun.com
- create
