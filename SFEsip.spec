#
# spec file for package SFEsip
#
# includes module(s): sip
#
%include Solaris.inc

%define python_version 2.4

Name:			SFEsip
Summary:		Python binding creator for C++ libraries
License:		Pythonish
Version:		4.7.4
Source:			http://www.riverbankcomputing.com/Downloads/sip4/sip-%{version}.tar.gz
URL:			http://www.riverbankcomputing.co.uk/sip
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWPython
%include default-depend.inc
BuildRequires: SUNWPython-devel

%prep
%setup -q -n sip-%{version}

%build
export PYTHON="/usr/bin/python2.4"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
python configure.py 
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages

# Delete optimized py code.
find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sip
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/python2.4/sip.h
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*

%changelog
* Sat Mar 29 2008 - laca@sun.com
- create
