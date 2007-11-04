#
# spec file for package SFEcompiz
#

%include Solaris.inc

%if %(pkginfo -q FSWxorg-clientlibs && echo 1 || echo 0)
# FOX
%define old_x11 0
%else
# Nevada X
%define old_x11     %(pkgchk -l SUNWxwinc 2>/dev/null | grep compositeproto >/dev/null && echo 0 || echo 1)
%endif

#%define gnome_2_20  %(pkg-config --atleast-version=2.19.0 libgnome-2.0 && echo 1 || echo 0)

Name:           SFEcompiz
Summary:        compiz
Version:        0.6.2
Source:		http://xorg.freedesktop.org/archive/individual/app/compiz-%{version}.tar.gz
Source1:	http://www.gnome.org/~erwannc/compiz/missing-stuff-%{version}.tar.bz2
Source2:	http://trisk.acm.jhu.edu/compiz/gnome-integration-%{version}.tar.bz2
Patch1:		compiz-01-solaris-port.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
Requires:	%name-root
Requires: 	SUNWpng
Requires: 	SUNWdbus
Requires: 	SUNWgnome-base-libs
Requires: 	SUNWgnome-wm
BuildRequires: 	SUNWpng-devel
BuildRequires: 	SUNWdbus-devel
BuildRequires: 	SUNWgnome-base-libs-devel
BuildRequires: 	SUNWgnome-wm-devel
BuildRequires: 	SFEsed

%package root
Summary:         %summary - platform dependent files, / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:		 %summary - developer files
sUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
%setup -q -c -n %{name}
gtar fxvj %{SOURCE1}
gtar fxvj %{SOURCE2}
cd compiz-%{version}
%patch1 -p1
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

PROTO_LIB=$RPM_BUILD_DIR/%{name}/usr/X11/lib
PROTO_INC=$RPM_BUILD_DIR/%{name}/usr/X11/include
PROTO_PKG=$RPM_BUILD_DIR/%{name}/usr/X11/lib/pkgconfig

export PKG_CONFIG_PATH="$PROTO_PKG"

export CFLAGS="%optflags -I$PROTO_INC -I/usr/include/startup-notification-1.0 -I/usr/X11/include" 
export LDFLAGS="-L$PROTO_LIB -L/usr/X11/lib -R/usr/X11/lib"

mkdir -p $PROTO_INC/X11/extensions
mkdir -p $PROTO_PKG
cp missing-stuff/missing-headers/Xregion.h $PROTO_INC/X11
cp missing-stuff/missing-pc-files/*.pc $PROTO_PKG

cd compiz-%{version}

intltoolize --copy --force --automake
aclocal
autoheader
automake -a -c -f
autoconf
 
export CFLAGS="%optflags -I$PROTO_INC -I/usr/include/startup-notification-1.0 -I/usr/X11/include" 
export LDFLAGS="-L$PROTO_LIB -L/usr/X11/lib -L/usr/openwin/lib -R/usr/X11/lib -R/usr/openwin/lib -lX11 -lXext"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}         \
	    --sysconfdir=%{_sysconfdir}	\
	    --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
	    --datadir=%{_datadir}	

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
cp missing-stuff/missing-pc-files/*.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mkdir -p  $RPM_BUILD_ROOT%{_prefix}/X11/include/X11
cp missing-stuff/missing-headers/Xregion.h $RPM_BUILD_ROOT%{_prefix}/X11/include/X11

cd compiz-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT/usr/X11/lib/*.la
rm -rf $RPM_BUILD_ROOT%{_basedir}/etc

cp start-compiz stop-compiz $RPM_BUILD_ROOT%{_bindir}
ln -s start-compiz $RPM_BUILD_ROOT%{_bindir}/run-compiz
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp compiz.png $RPM_BUILD_ROOT%{_datadir}/pixmaps

cd $RPM_BUILD_ROOT%{_libdir}/pkgconfig
for pc in ice.pc sm.pc; do
    test -f /usr/lib/pkgconfig/$pc && rm $pc
done


%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif


%post root
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/compiz-annotate.schemas \
                                                                                           /etc/gconf/schemas/compiz-blur.schemas \
                                                                                           /etc/gconf/schemas/compiz-clone.schemas \
                                                                                           /etc/gconf/schemas/compiz-core.schemas \
                                                                                           /etc/gconf/schemas/compiz-cube.schemas \
                                                                                           /etc/gconf/schemas/compiz-dbus.schemas \
                                                                                           /etc/gconf/schemas/compiz-decoration.schemas \
                                                                                           /etc/gconf/schemas/compiz-fade.schemas \
                                                                                           /etc/gconf/schemas/compiz-fs.schemas \
                                                                                           /etc/gconf/schemas/compiz-gconf.schemas \
                                                                                           /etc/gconf/schemas/compiz-glib.schemas \
                                                                                           /etc/gconf/schemas/compiz-ini.schemas \
                                                                                           /etc/gconf/schemas/compiz-inotify.schemas \
                                                                                           /etc/gconf/schemas/compiz-minimize.schemas \
                                                                                           /etc/gconf/schemas/compiz-move.schemas \
                                                                                           /etc/gconf/schemas/compiz-place.schemas \
                                                                                           /etc/gconf/schemas/compiz-plane.schemas \
                                                                                           /etc/gconf/schemas/compiz-png.schemas \
                                                                                           /etc/gconf/schemas/compiz-regex.schemas \
                                                                                           /etc/gconf/schemas/compiz-resize.schemas \
                                                                                           /etc/gconf/schemas/compiz-rotate.schemas \
                                                                                           /etc/gconf/schemas/compiz-scale.schemas \
                                                                                           /etc/gconf/schemas/compiz-screenshot.schemas \
                                                                                           /etc/gconf/schemas/compiz-svg.schemas \
                                                                                           /etc/gconf/schemas/compiz-switcher.schemas \
                                                                                           /etc/gconf/schemas/compiz-video.schemas \
                                                                                           /etc/gconf/schemas/compiz-water.schemas \
                                                                                           /etc/gconf/schemas/compiz-wobbly.schemas \
                                                                                           /etc/gconf/schemas/compiz-zoom.schemas \
                                                                                           /etc/gconf/schemas/gwd.schemas

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/compiz
%dir %attr (0755, root, bin) %{_libdir}/window-manager-settings
%{_libdir}/lib*so*
%{_libdir}/compiz/lib*so*
%{_libdir}/window-manager-settings/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/compiz
%dir %attr(0755, root, other) %{_datadir}/gnome
%dir %attr(0755, root, bin) %{_datadir}/gnome/wm-properties
%dir %attr(0755, root, bin) %{_datadir}/gnome-control-center
%dir %attr(0755, root, bin) %{_datadir}/gnome-control-center/keybindings
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/compiz/*
%{_datadir}/gnome/wm-properties/compiz.desktop
%{_datadir}/gnome-control-center/keybindings/*
%{_datadir}/pixmaps/*

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_prefix}/X11
%dir %attr (0755, root, bin) %{_prefix}/X11/include
%dir %attr (0755, root, bin) %{_prefix}/X11/include/X11
%{_prefix}/X11/include/X11/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Nov 04 2007 - erwann@sun.com
- remove unneeded X bits
- lighter version of missing-stuff
- ship missing X header
* Mon Oct 29 2007 - trisk@acm.jhu.edu
- Bump to 0.6.2
- Don't create icons in gnome-integration (use fusion-icon)
* Tue Oct 16 2007 - laca@sun.com
- add FOX build support
* Fri Sep 21 2007 - Albert Lee <trisk@acm.jhu.edu>
- Add optional patch for "black windows" workaround
- Fix install in GNOME 2.19/2.20
* Thu Sep 06 2007 - Albert Lee <trisk@acm.jhu.edu>
- Updated to coexist with newer X consolidation packages
* Wed Mar 08 2007 - Doug Scott <dougs at truemail.co.th>
- Changed to build on un-modified system
* Tue Mar 06 2007 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
