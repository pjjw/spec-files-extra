#
# spec file for package SFEgnome-gvfs
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

%use gvfs = gvfs.spec

Name:                    SFEgnome-gvfs
Summary:                 GNOME virtual file system framework
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWdbus
Requires: SUNWlibmsr
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWdbus-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%gvfs.prep -d %name-%version

%build
# -D_XPG4_2 is to get CMSG_SPACE declaration in <sys/socket.h>.
export CFLAGS="%optflags -D_XPG4_2 -D__EXTENSIONS__"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
%gvfs.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gvfs.install -d %name-%version
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gvfs/modules/*.la

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
