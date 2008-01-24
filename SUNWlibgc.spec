#
# spec file for package SUNWlibgc
#
# includes module(s): libgc
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%include Solaris.inc

%use libgc = libgc.spec

Name:                    SUNWlibgc
Summary:                 Boehm-Demers-Weiser garbage collector for C/C++
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWcsl
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
rm -rf %name-%version
mkdir %name-%version
%libgc.prep -d %name-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

%libgc.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libgc.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gc

%changelog
* Thu Jan 03 2008 - nonsea@users.sourceforge.net
- Use base spec libgc.spec
* Mon Oct 15 2007 - nonsea@users.sourceforge.net
- Bump to 7.0
- s/gc%{version}/gc-%{version}/g
- Add *.pc to %files devel
* Thu Jul  6 2006 - laca@sun.com
- rename to SFEhp-gc
- delete -share subpkg
- update file attributes
- delete unnecessary env variables
* Mon Jan 30 2006 - glynn.foster@sun.com
- Initial version
