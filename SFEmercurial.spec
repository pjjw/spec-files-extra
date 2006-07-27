#
# spec file for package SFEmercurial
#
# includes module(s): mercurial
#
%include Solaris.inc

%define python_version 2.4

Name:			SFEmercurial
License:		GPL
Group:			system/dscm
Version:		0.9
Release:		1
Summary:		Mercurial SCM
Source:			http://www.selenic.com/mercurial/release/mercurial-%{version}.tar.gz
URL:			http://www.selenic.com
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
%include default-depend.inc
Requires: SUNWPython
Requires: SUNWcsr

%description
Mercurial source code management system.

%prep
%setup -q -n mercurial-%{version}

%build
export PYTHON="/usr/bin/python"
CFLAGS="$RPM_OPT_FLAGS"
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
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
%{_libdir}

%changelog
* Fri Jul  7 2006 - laca@sun.com
- rename to SFEmercurial
- update file attributes
* Sun Jun  4 2006  <dougs@truemail.co.th>
- bumped to v0.9
- removed patch which is no longer needed
- changed python perms to same as delevered in snv40
* Sat Jan  7 2006  <glynn.foster@sun.com>
- initial version
