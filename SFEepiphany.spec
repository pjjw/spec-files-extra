#
# spec file for package SFEepiphany
#
# includes module(s): gvfs
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
%include Solaris.inc

%use epiphany = epiphany.spec

Name:                    SFEepiphany
Summary:                 GNOME web browser - epiphany
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWfirefox
Requires: SUNWdbus
Requires: SUNWlibmsr
Requires: SUNWprd
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWfirefox-devel
BuildRequires: SUNWprd

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%epiphany.prep -d %name-%version

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
export PKG_CONFIG_PATH=%{_datadir}/pkgconfig:%{_pkg_config_path}
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
export CXXFLAGS="$CXXFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
%epiphany.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%epiphany.install -d %name-%version
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gvfs-daemon*
%{_libdir}/libgvfscommon.so*
%{_libdir}/gio/modules/*.so*
%{_libdir}/gvfs/modules/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1/services/gvfs-daemon.service

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gvfs


%changelog
* Thu Nov 07 2007 - damien.carbery@sun.com
- Initial version.
