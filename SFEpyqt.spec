#
# spec file for package SFEpyqt
#
# includes module(s): 
#
%include Solaris.inc

%define python_version 2.4

Name:			SFEpyqt
Summary:		Python interface to Qt
License:		GPL
Version:		3.17.4
Source:			http://www.riverbankcomputing.com/Downloads/PyQt3/GPL/PyQt-x11-gpl-%{version}.tar.gz
URL:			http://www.riverbankcomputing.co.uk/pyqt/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWPython
%include default-depend.inc
Requires: SFEqt3
BuildRequires: SUNWPython-devel
BuildRequires: SFEsip

%prep
%setup -q -n PyQt-x11-gpl-%{version}

%build
export PYTHON="/usr/bin/python2.4"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export QMAKESPEC=/usr/share/qt3/mkspecs/default
echo yes | python configure.py -w \
    -q /usr \
    -d %{_libdir}/python2.4/vendor-packages
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Delete optimized py code.
find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/pylupdate
%{_bindir}/pyuic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/sip

%changelog
* Sat Mar 29 2008 - laca@sun.com
- create
