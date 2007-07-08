#
# spec file for package SFEcompiz
#

%include Solaris.inc

Name:           SFEcompiz
Summary:        compiz
Version:        0.5.0
Source:		http://xorg.freedesktop.org/archive/individual/app/compiz-%{version}.tar.gz
Source1:	http://www.gnome.org/~erwannc/compiz/missing-stuff.tar.bz2
Source2:	http://xorg.freedesktop.org/releases/X11R7.2/src/lib/libXrender-X11R7.2-0.9.2.tar.bz2
Source3:	http://ftp.x.org/pub/individual/proto/compositeproto-0.3.1.tar.bz2
Source4:	http://ftp.x.org/pub/individual/proto/damageproto-1.1.0.tar.bz2
Source5:	http://ftp.x.org/pub/individual/proto/renderproto-0.9.2.tar.bz2
#Source6:	http://ftp.x.org/pub/individual/proto/xproto-7.0.10.tar.bz2
Source7:	http://ftp.x.org/pub/individual/lib/libXcomposite-0.3.1.tar.bz2
Patch1:		compiz-01-solaris-port.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
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
gtar fxvj %{SOURCE3}
gtar fxvj %{SOURCE4}
gtar fxvj %{SOURCE5}
#gtar fxvj %{SOURCE6}
gtar fxvj %{SOURCE7}
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

export CFLAGS="%optflags -I$PROTO_INC -I/usr/include/startup-notification-1.0" 
export LDFLAGS="-L$PROTO_LIB -R/usr/X11/lib"

mkdir -p $PROTO_INC/X11/extensions
mkdir -p $PROTO_PKG
cp missing-stuff/missing-headers/Xregion.h $PROTO_INC/X11
cp missing-stuff/missing-pc-files/*.pc $PROTO_PKG

for i in compositeproto-0.3.1 damageproto-1.1.0 renderproto-0.9.2
do
  cd $i
  ./configure --prefix=/usr/X11
  make
  make install DESTDIR=$RPM_BUILD_DIR/%{name}
  cd ..
done

cd libXrender-X11R7.2-0.9.2
./configure --prefix=/usr/X11 --disable-static
make
make install DESTDIR=$RPM_BUILD_DIR/%{name}
/usr/gnu/bin/sed -i \
	-e "s+Libs: +Libs: -L$PROTO_LIB +"	\
	-e "s+Cflags: +Cflags: -I$PROTO_INC +"	\
	$PROTO_PKG/xrender.pc
cd ..

cd libXcomposite-0.3.1
./configure --prefix=/usr/X11 --disable-static
make install DESTDIR=$RPM_BUILD_DIR/%{name}
/usr/gnu/bin/sed -i \
	-e "s+Libs: +Libs: -L$PROTO_LIB +"	\
	-e "s+Cflags: +Cflags: -I$PROTO_INC +"	\
	$PROTO_PKG/xcomposite.pc

cd ..
find usr -name \*.la -exec rm {} \;
find usr -name \*.a -exec rm {} \;
cd compiz-%{version}

aclocal
autoheader
automake -a -c -f
autoconf
 
export CFLAGS="%optflags -I$PROTO_INC -I/usr/include/startup-notification-1.0" 
export LDFLAGS="-L$PROTO_LIB -L/usr/X11/lib -L/usr/openwin/lib -R/usr/X11/lib -R/usr/openwin/lib -lX11 -lXext"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}         \
	    --sysconfdir=%{_sysconfdir}	\
	    --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
	    --datadir=%{_datadir}	\
	    --with-default-plugins="png,decoration,wobbly,animation,fade,minimize,cube,switcher,move,resize,place,rotate,zoom,scale,dbus,water,snow,trailfocus,thumbnail,ring"

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
PROTO_PKG=$RPM_BUILD_DIR/%{name}/usr/X11/lib/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
cp ${PROTO_PKG}/*.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig

for i in compositeproto-0.3.1 libXcomposite-0.3.1  libXrender-X11R7.2-0.9.2 compiz-%{version}
do
    cd $i
    make install DESTDIR=$RPM_BUILD_ROOT
    cd ..
done


rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/compiz/*.la
rm $RPM_BUILD_ROOT%{_libdir}/compiz/*.a
rm $RPM_BUILD_ROOT%{_libdir}/window-manager-settings/*.la
rm $RPM_BUILD_ROOT%{_libdir}/window-manager-settings/*.a
rm $RPM_BUILD_ROOT/usr/X11/lib/*.la
rm -rf $RPM_BUILD_ROOT%{_basedir}/etc
mv $RPM_BUILD_ROOT/usr/X11/lib/pkgconfig/* $RPM_BUILD_ROOT/usr/lib/pkgconfig
rmdir $RPM_BUILD_ROOT/usr/X11/lib/pkgconfig
rm -rf $RPM_BUILD_ROOT/usr/X11/share

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif


%post root
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/compiz.schemas

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
%{_datadir}/gnome/wm-properties/compiz.desktop
%{_datadir}/compiz/*
%dir %attr (0755, root, bin) %{_prefix}/X11
%dir %attr (0755, root, bin) %{_prefix}/X11/lib
%{_prefix}/X11/lib/lib*.so*


%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/compiz.schemas
%{_sysconfdir}/gconf/schemas/gwd.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_prefix}/X11
%dir %attr (0755, root, bin) %{_prefix}/X11/include
%{_prefix}/X11/include/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Mar 08 2007 - Doug Scott <dougs at truemail.co.th>
- Changed to build on un-modified system
* Tue Mar 06 2007 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
