#http://www.sun.com/third-party/global/opensource.jsp
# spec file for package SFEvalknut
#
# includes module(s): valknut dclib
#
%include Solaris.inc

%include base.inc

%use valknut = valknut.spec
%use dclib = dclib.spec

Name:		SFEvalknut
Summary:	%{valknut.summary}
Version:	%{valknut.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEqt
BuildRequires: SFEqt
Requires: SUNWlxml
BuildRequires: SUNWlxml

%prep
rm -rf %name-%version
mkdir %name-%version

%valknut.prep -d %name-%version
%dclib.prep -d %name-%version

%build
DCLIB_ROOT=%{_builddir}/%name-%version/%{dclib.name}-%{dclib.version}
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CXXFLAGS="%{gcc_cxx_optflags} -I$DCLIB_ROOT/dclib -I$DCLIB_ROOT/dclib/core"
export LDFLAGS="%_ldflags -L$DCLIB_ROOT/dclib/.libs"

export PKG_CONFIG_PATH="%{_libdir}/pkgconfig:$DCLIB_ROOT"

%dclib.build -d %name-%version
%valknut.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%dclib.install -d %name-%version
%valknut.install -d %name-%version
rm -f $RPM_BUILD_ROOT%{_libdir}/libdc.*a
rm -rf $RPM_BUILD_ROOT%{_libdir}/dclib
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig
rm -rf $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/valknut
%{_datadir}/valknut/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/64x64/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/64x64/apps/
%{_datadir}/icons/hicolor/64x64/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/apps/
%{_datadir}/icons/hicolor/128x128/apps/*

%changelog
* Tue Nov 4 2008 - Andras Barna (andras.barna@gmail.com)
- Initial spec file

