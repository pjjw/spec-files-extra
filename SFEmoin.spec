#
# In theory this package could be named SFEpython-moin instead of
# SFEmoin, but when a python (or perl or php) package delivers an
# application or command(s) like this one does (as opposed to a library), it
# seems to make more sense to omit the language name from the package name.
#
#
%include Solaris.inc

Name:                SFEmoin
Summary:             Clone of WikiWiki
Version:             1.5.7
Source:              http://%{sf_mirror}/sourceforge/moin/moin-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
Requires: SUNWPython

%prep
%setup -q -n moin-%version

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
%dir %attr (0755, root, bin) %{_datadir}/moin
%{_datadir}/moin/*

%changelog
* 
* Sat Mar 31 2007 - Eric Boutilier
- Initial spec
- Python App: Clone of WikiWiki
