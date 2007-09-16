#
# spec file for package SFEpida
#
# includes module(s): PIDA
#
%include Solaris.inc

%define python_version 2.4

Name:			SFEpida
Summary:		A Python Integrated Development Environment
Version:		0.5.1
Source:			http://pida.googlecode.com/files/PIDA-%{version}.tar.gz
URL:			https://launchpad.net/pida
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_prefix}

%include default-depend.inc

Requires: SUNWPython
Requires: SFEkiwi
Requires: SFEvim
Requires: SUNWgnome-terminal
Requires: SUNWgnome-python-libs
BuildRequires: SUNWPython-devel
BuildRequires: SUNWgnome-terminal-devel
BuildRequires: SUNWgnome-python-libs-devel

%prep
%setup -q -n PIDA-%{version}

%build
export CFLAGS="-I moo"
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/site-packages/*

%changelog
* Sun Sep 16 2007 - Ananth Shrinivas <ananth@sun.com>
- Created new spec.

