#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define with_libgsf %(pkginfo -q SFElibgsf && echo 1 || echo 0)
%define with_w3m    %(pkginfo -q SFEw3m && echo 1 || echo 0)
%define with_mv     %(pkginfo -q SFEwv && echo 1 || echo 0)

Name:           SFEtracker
License:        GPL
Summary:        Desktop search tool
Version:        0.6.0
URL:            http://www.tracker-project.org
Source:         http://www.gnome.org/~jamiemcc/tracker/tracker-%{version}.tar.gz
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:       SUNWgnome-base-libs
Requires:       SUNWdbus
Requires:       SUNWzlib
Requires:       SFEsqlite
Requires:       SFEgmime
Requires:       OSOLgamin
BuildRequires:  SUNWgnome-base-libs-devel
BuildRequires:  SUNWdbus-devel
BuildRequires:  SFEgmime-devel
BuildRequires:  SFEsqlite-devel
BUildRequires:  OSOLgamin-devel
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
%if %with_libgsf
Requires:       SFElibgsf
BuildRequires:  SFElibgsf-devel
%endif
%if %with_w3m
Requires:       SFEw3m
%endif
%if %with_w3m
Requires:       SFEwv
BuildRequires:  SFEwv-devel
%endif

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
%{_libdir}/tracker
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/tracker
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/tracker.service
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%defattr (-, root, other)
%{_datadir}/icons

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
* Fri Jul 24 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.0.
- Remove dependency on file.
* Fri May 04 2007 - nonsea@users.sourceforge.net
- Add Requires to SFEsqlite
- Add conditional Requires to SFEwv
- Revert patch tracker-01-stdout.diff.
- Add attr (0755, root, other) to %{_datadir}/pixmaps
  and %{_datadir}/applications
* Fri May 04 2007 - nonsea@users.sourceforge.net
- Add conditional Require SFElibgsf SFEw3m
- Remove upstreamed patch tracker-01-stdout.diff
- Add URL and License.
* Fri May 04 2007 - nonsea@users.sourceforge.net
- Initial spec
