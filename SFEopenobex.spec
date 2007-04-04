#
# spec file for package SFEopenobex
#
# includes module(s): openobex
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%use openobex = openobex.spec

Name:               SFEopenobex
Summary:            OpenOBEX - open source implementation of the Object Exchange protocol
Version:            %{openobex.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SUNWlibusb

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%openobex.prep -d %name-%version

%build
export CFLAGS="-I/usr/sfw/include %optflags"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
export RPM_OPT_FLAGS="$CFLAGS"
export PKG_CONFIG_PATH=%{_builddir}/%name-%version/openobex-%{openobex.version}
%openobex.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%openobex.install -d %name-%version
rmdir $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Mon Apr  2 2007 - laca@sun.com
- initial version created
