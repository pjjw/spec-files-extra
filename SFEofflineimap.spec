#   
#
%include Solaris.inc

Name:                SFEofflineimap
Summary:             Bi-directional sync'ing of IMAP/Maildir email boxes
Version:             4.0.15
Source:              http://software.complete.org/offlineimap/static/download_area/4.0.15/offlineimap_%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
Requires: SUNWPython

%prep
%setup -q -n offlineimap

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

%changelog
* 
* Sat Mar 31 2007 - Eric Boutilier
- Initial spec
- Python App: Two-way sync of IMAP/Maildir email boxes
