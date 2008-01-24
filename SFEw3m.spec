#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%include Solaris.inc

%use w3m = w3m.spec

Name:                SFEw3m
Summary:             A text-based web browser
Version:             %{default_pkg_version}
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:            SUNWgnome-base-libs
Requires:            SUNWlibmsr
Requires:            SUNWperl584core
%if %option_with_fox
Requires: FSWxorg-clientlibs
Requires: FSWxwrtl
BuildRequires: FSWxorg-headers
%else
Requires: SUNWxwrtl
%endif
Requires:            SUNWzlib
Requires:            SUNWlibgc
Requires:            SUNWopenssl-libraries
BuildRequires:       SUNWgnome-base-libs-devel
BuildRequires:       SUNWopenssl-include
BuildRequires:       SUNWlibgc-devel
Conflicts:           SUNWdesktop-search-libs

%prep
rm -rf %name-%version
mkdir %name-%version
%w3m.prep -d %name-%version

%build

export CFLAGS="%optflags -I/usr/sfw/include"
%if %option_with_fox
export CFLAGS="$CFLAGS -I/usr/X11/include"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags -lX11 -L/usr/sfw/lib -R/usr/sfw/lib"

%w3m.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%w3m.install -d %name-%version

#remove unused files
rm -rf $RPM_BUILD_ROOT%{_mandir}/ja

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/w3m/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man*/*

%changelog
* Thu Jan 03 2008 - nonsea@users.sourceforge.net
- Use base spec w3m.spec
* Sat Nov 17 2007 - daymobrew@users.sourceforge.net
- Add support for building on Indiana system.
* Tue Sep 18 2007 - nonsea@users.sourceforge.net
- Add URL
* Tue Sep 11 2007 - nonsea@users.sourceforge.net
- Add --with-browser=/usr/bin/firefox, replace default value mozilla.
* Wed Sep 05 2007 - nonsea@users.sourceforge.net
- Bump to 0.5.2
* Thu May 03 2007 - nonsea@users.sourceforge.net
- Initial spec
