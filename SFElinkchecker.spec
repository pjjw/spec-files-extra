#   
#
%include Solaris.inc

Name:                SFElinkchecker
Summary:             URL link checker
Version:             4.6
Source:              http://superb-east.dl.sourceforge.net/sourceforge/linkchecker/linkchecker-4.6.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
Requires: SUNWPython

%prep
%setup -q -n linkchecker-%version

%build
# Bypass build because the Python distutils (setup.py) standard specifies 
# that the install step (below) implicitly does a build anyway.
exit 0

%install
# The %prefix setting and any other build/install vars are set automatically.
# See /usr/lib/python2.4/config/Makefile. Thus, it is possible (in fact,
# preferred IMO) to not specify any here, except, of course, $RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT
/usr/bin/python2.4 ./setup.py install --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/de
%{_mandir}/de/*
%dir %attr (0755, root, bin) %{_mandir}/fr
%{_mandir}/fr/*
%dir %attr (0755, root, other) %{_datadir}/linkchecker
%{_datadir}/linkchecker/*

%changelog
* 
* Sat Mar 31 2007 - Eric Boutilier
- Initial spec
- Python App: URL link checker
