#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%use tracker = tracker.spec

Name:           SFEtracker
Summary:        tracker.summary
Version:        %{default_pkg_version}
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source1:        tracker-firefox-history-xesam.xpi
Source2:        tracker-thunderbird.xpi
%include default-depend.inc
Requires:       SUNWgnome-base-libs
Requires:       SUNWdbus
Requires:       SUNWzlib
Requires:       SFEsqlite
Requires:       SFEgmime
Requires:       SUNWgamin
BuildRequires:  SUNWgnome-base-libs-devel
BuildRequires:  SUNWdbus-devel
BuildRequires:  SFEgmime-devel
BuildRequires:  SFEsqlite-devel
BUildRequires:  SUNWgamin-devel
#Additional recommended packages
Requires:       SUNWgnome-media
Requires:       SUNWpng
Requires:       SUNWogg-vorbis
Requires:       SUNWlibexif
Requires:       SUNWgnome-pdf-viewer
Requires:       SUNWlxsl
Requires:       SFEw3m
Requires:       SFEwv
Requires:       SFElibgsf
BuildRequires:  SUNWgnome-media-devel
BuildRequires:  SUNWpng-devel
BuildRequires:  SUNWogg-vorbis-devel
BuildRequires:  SUNWlibexif-devel
BuildRequires:  SUNWgnome-pdf-viewer-devel
BuildRequires:  SUNWlxsl-devel
BuildRequires:  SFEwv-devel
BuildRequires:  SFElibgsf-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package extension 
Summary:        %{summary} - extension files
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
rm -rf %name-%version
mkdir -p %name-%version
%tracker.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export RPM_OPT_FLAGS="$CFLAGS"
%tracker.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%tracker.install -d %name-%version
cd %{_builddir}/%name-%version

# Install firefox extension
mkdir -p $RPM_BUILD_ROOT%{_libdir}/firefox/extensions
cd $RPM_BUILD_ROOT%{_libdir}/firefox/extensions
mkdir \{fda00e13-8c62-4f63-9d19-d168115b11ca\}
cd \{fda00e13-8c62-4f63-9d19-d168115b11ca\}
unzip %SOURCE1

# Install firefox extension
mkdir -p $RPM_BUILD_ROOT%{_libdir}/thunderbird/extensions
cd $RPM_BUILD_ROOT%{_libdir}/thunderbird/extensions
mkdir \{b656ef18-fd76-45e6-95cc-8043f26361e7\}
cd \{b656ef18-fd76-45e6-95cc-8043f26361e7\}
unzip %SOURCE2

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
%dir %attr (0755, root, bin) %{_libdir}/deskbar-applet
%dir %attr (0755, root, bin) %{_libdir}/deskbar-applet/modules-2.20-compatible
%{_libdir}/deskbar-applet/modules-2.20-compatible/tracker-module.py
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

%files extension
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/firefox
%{_libdir}/thunderbird

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
* Fri Nov 02 2007 - nonsea@users.sourceforge.net
- Remove useless gnu staff from CFLAGS and LDFLAGS.
* Fri Nov 02 2007 - nonsea@users.sourceforge.net
- Spilit into base/tracker.spec
- Remove GNOMOE 2.19/2.20 install compatible part.
- Add package -extension to install firefox/thunderbird extensions.
* Fri Sep 28 2007 - nonsea@users.sourceforge.net
- Add patch thunderbird.diff to enable thunderbird index.
* Wed Sep 26 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.3.
- Move wv and libgsf to Requires.
- Add patch w3m-crash to fix w3m crash on solaris.
* Fri Sep 21 2007 - trisk@acm.jhu.edu
- Fix install in GNOME 2.19/2.20
* Wed Sep 05 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.2.
- Move w3m to Requires.
* Thu Aug 09 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.1.
* Mon Aug 06 2007 - nonsea@users.sourceforge.net
- Add --enable-external-sqlite
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
