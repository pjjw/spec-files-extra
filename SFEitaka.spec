#
# spec file for package SFEitaka
#
# includes module(s): itaka
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                    SFEitaka
Summary:                 On-demand screen capture server
Version:                 0.2
Source:                  http://downloads.sourceforge.net/itaka/itaka-%{version}.tar.bz2
Patch1:                  itaka-01-manfix.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}_%{version}-build
%include default-depend.inc

Requires:    SUNWgnome-python-libs-devel
Requires:    SUNWpython-twisted
Requires:    SUNWPython

%prep
rm -rf %name-%version
%setup -q -n itaka-%version

%patch1 -p1

%install

rm -rf $RPM_BUILD_ROOT
make -f Makefile.Debian install DESTDIR=$RPM_BUILD_ROOT
( cd vuze && cp -rp * $RPM_BUILD_ROOT%{_libdir}/itaka/ )
rm -f $RPM_BUILD_ROOT%{_bindir}/itaka
ln -s ../lib/itaka/itaka.py $RPM_BUILD_ROOT%{_bindir}/itaka

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/itaka
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755,root,sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/itaka.desktop
%dir %attr (0755, root, other) %{_datadir}/itaka
%{_datadir}/itaka/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/itaka.1

%changelog
* Tue Jul 01 2008 - Andras Barna (andras.barna@gmail.com)
- Initial spec
