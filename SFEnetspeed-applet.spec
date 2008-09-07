#
# spec file for package SFEnetspeed-applet
#
# includes module(s): netspeed_applet
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                    SFEnetspeed-applet
Summary:                 Netspeed applet for GNOME
Group:                   System/GUI/GNOME
Version:                 0.15
Source:                  http://www.wh-hms.uni-ulm.de/~mfcn/netspeed/packages/netspeed_applet-%{version}.tar.gz
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}_%{version}-build
%include default-depend.inc

Requires:    SUNWgnome-libs
Requires:    SUNWgnome-panel
Requires:    SUNWlibgtop
BuildRequires:    SUNWgnome-libs-devel
BuildRequires:    SUNWgnome-panel-devel
BuildRequires:    SUNWlibgtop-devel
BuildRequires:    SUNWgnome-common-devel
BuildRequires:    SUNWperl-xml-parser

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name_%version
%setup -q -n netspeed_applet-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags -lnsl -lsocket"

aclocal
automake -a -f
autoconf -f

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*
%dir %attr (0755, root, bin) %{_datadir}/omf
%{_datadir}/omf/*
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/devices
%{_datadir}/icons/hicolor/16x16/devices/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/status
%{_datadir}/icons/hicolor/24x24/status/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Sep 07 2008 - Andras Barna (andras.barna@gmail.com)
- New version, remove patch01, fixed upstream
* Sun Aug 03 2008 - Andras Barna (andras.barna@gmail.com)
- Opensolaris fixes.
* Mon Jun 30 2008 - Andras Barna (andras.barna@gmail.com)
- Fix permissions
* Thu Jun 23 2008 - Andras Barna (andras.barna@gmail.com)
- Initial spec
