#
# spec file for package gnome-power-manager
#
#
Name:           gnome-power-manager
License:        GPL
Group:		X11/Applications
Version:        2.21.1
Release:        2
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Summary:	GNOME Power Manager
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-power-manager/2.21/%{name}-%{version}.tar.bz2
Patch1:         gnome-power-manager-01-build.diff
# set gconf key "cpufreq_show" as "true" by default and define
# gconf key "icon_policy" as "always" by default.
Patch6:		gnome-power-manager-06-icon_plicy_and_cpufreq_show.diff
Patch7:         gnome-power-manager-07-disable-sleep-configration.diff
Patch8:		gnome-power-manager-08-brightness-applet-install.diff
Patch9:		gnome-power-manager-09-scripts.diff
URL:		http://www.gnome.org/projects/gnome-power-manager/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.73
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-keyring-devel >= 0.8
BuildRequires:	gnome-panel-devel >= 2.18.0
BuildRequires:	gtk+2-devel >= 1:2.10.10
BuildRequires:	hal-devel >= 0.5.7.1
BuildRequires:	intltool >= 0.35.5
BuildRequires:	libglade2-devel >= 2.6.0
BuildRequires:	libgnomeui-devel >= 2.18.0
BuildRequires:	libnotify-devel >= 0.4.3
BuildRequires:	libtool
BuildRequires:	libwnck-devel >= 2.18.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper
Requires:	GConf2
Requires:	gtk+2
Requires:	hicolor-icon-theme
Requires:	scrollkeeper
Requires:	gnome-session >= 2.18.0
Requires:	notification-daemon >= 0.3.5
Obsoletes:	gnome-power
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Uses of GNOME Power Manager infrastructure
- A dialogue that warns the user when on UPS power, that automatically
  begins a kind shutdown when the power gets critically low.
- An icon that allows a user to dim the LCD screen with a slider, and
  does do automatically when going from mains to battery power on a
  laptop.
- An icon, that when an additional battery is inserted, updates it's
  display to show two batteries and recalculates how much time
  remaining. Would work for wireless mouse and keyboards, UPS's and
  PDA's.
- A daemon that does a clean shutdown when the battery is critically
  low or does a soft-suspend when you close the lid on your laptop (or
  press the "suspend" button on your PC).
- Tell Totem to use a codec that does low quality processing to
  conserve battery power.
- Postpone indexing of databases (e.g. up2date) or other heavy
  operations until on mains power.
- Presentation programs / movie players don't want the screensaver
  starting or screen blanking.

%prep
%setup -q
%patch1 -p1
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p0

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

intltoolize --copy --force --automake
autoheader
autoconf
./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info
	    		
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT \
	
%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install gnome-power-manager.schemas
%preun
%gconf_schema_uninstall gnome-power-manager.schemas

%postun
%scrollkeeper_update_postun

%files
%defattr(-,root,root)
%{_libdir}/bonobo/servers/GNOME_BrightnessApplet.server
%{_libdir}/bonobo/servers/GNOME_InhibitApplet.server
%{_datadir}/gnome/autostart/gnome-power-manager.desktop
%{_datadir}/dbus-1/services/gnome-power-manager.service
%{_datadir}/gnome-2.0/ui/GNOME_BrightnessApplet.xml
%{_datadir}/gnome-2.0/ui/GNOME_InhibitApplet.xml
%{_mandir}/man1/*.1*
%{_datadir}/gnome-power-manager/*
%{_sysconfdir}/gconf/schemas/gnome-power-manager.schemas


%changelog
* Tue Dec 18 2007 - simon.zheng@sun.com
- Rework gnome-power-manager-07-disable-sleep-configration.diff.
- Rework gnome-power-manager-08-brightness-applet-install.diff.
- Add gnome-power-manager-09-scripts.diff.

* Mon Dec 17 2007 - simon.zheng@sun.com
- Bump to 2.21.1.
- Rework gnome-power-manager-01-build.diff.
- Remove gnome-power-manager-02-kstat.diff.
- Remove upstream patch gnome-power-manager-03-brightness-get-stuck.diff.
- Remove gnome-power-manager-04-display-sleep.diff.
- Remove gnome-power-manager-05-configure-power-conf.diff
- Add gnome-power-manager-07-disable-sleep-configration.diff.
- Add gnome-power-manager-08-brightness-applet-install.diff.

* Thu Dec 12 2007 - simon.zheng@sun.com
- Add patch gnome-power-manager-06-icon_plicy_and_cpufreq_show.diff,
  set gconf key "cpufreq_show" as true by default and define
  gconf key "icon_policy" as always by default.

* Fri Dec 07 2007 - simon.zheng@sun.com
- Update patch gnome-power-manager-05-configure-power-conf.diff.

* Thu Dec 06 2007 - simon.zheng@sun.com
- Add patch gnome-power-manager-05-configure-power-conf.diff
  to make autoS3, autoshutdwon, disk powermanagement, autopm
  work on Solaris.

* Wed Nov 28 2007 - simon.zheng@sun.com
- Add patch gnome-power-manager-04-display-sleep.diff, to
  make display sleeping work.

* Fri Nov 17 2007 - simon.zheng@sun.com
- Bump to version 2.20.1
- Add patch gnome-power-manager-03-brightness-get-stuck.diff.
  to fix bugzilla bug #497298,

* Wed Sep 19 2007 - trisk@acm.jhu.edu
- Add intltoolize to fix build

* Wed Sep 19 2007 - simon.zheng@sun.com
- Bump to version 2.20.0

* Tue Aug 28 2007 - jeff.cai@sun.com
- Bump to version 2.19.6.

* Tue May 15 2007 - simon.zheng@sun.com
- Bump to version 2.19.2.

* Mon May 14 2007 - simon.zheng@sun.com
- Add a patch gnome-power-manager-02-kstat.diff to 
  port cpu usage statistic to solaris.

* Tue May 08 2007 - simon.zheng@sun.com
- Bump to version 2.19.1

* Fri Apr 27 2007 - simon.zheng@sun.com
- Bump to version 2.18.2

* Tue Mar 28 2007 - simon.zheng@sun.com
- initial version for pkgbuild
