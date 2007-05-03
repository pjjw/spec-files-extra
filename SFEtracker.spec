#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define with_gstremer %(pkginfo -q SUNWgnome-media-devel && echo 1 || echo 0)
%define with_libpng   %(pkginfo -q SUNWpng-devel && echo 1 || echo 0)
%define with_libvorbis %(pkginfo -q SUNWogg-vorbis-devel && echo 1 || echo 0)
%define with_libexif %(pkginfo -q SUNWlibexif-devel && echo 1 || echo 0)

Name:		SFEtracker
Summary:	Desktop search tool
Version:	0.5.4
Source:		http://www.gnome.org/~jamiemcc/tracker/tracker-%{version}.tar.gz
Patch1:		tracker-01-stdout.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:       SUNWgnome-base-libs
Requires:       SUNWdbus
Requires:       SUNWzlib
Requires:       SFEfile
Requires:       SFEgmime
BuildRequires:  SUNWgnome-base-libs-devel
BuildRequires:  SUNWdbus-devel
BuildRequires:  SFEfile
BuildRequires:  SFEgmime-devel
#Additional recommended packages
Requires:       SUNWgnome-media
Requires:       SUNWpng
Requires:       SUNWogg-vorbis
Requires:       SUNWlibexif
Requires:       SUNWgnome-pdf-viewer
Requires:       SUNWlxsl
BuildRequires:  SUNWgnome-media-devel
BuildRequires:  SUNWpng-devel
BuildRequires:  SUNWogg-vorbis-devel
BuildRequires:  SUNWlibexif-devel
BuildRequires:  SUNWgnome-pdf-viewer-devel
BuildRequires:  SUNWlxsl-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n tracker-%version
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

./configure --prefix=%{_prefix}  \
	    --sysconfdir=%{_sysconfdir} \
            --disable-warnings

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/deskbar-applet
%{_libdir}/tracker
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/tracker
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/tracker
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/tracker.service
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Feb 08 2007 - jedy.wang@sun.com
- Initial spec
