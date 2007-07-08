#
# spec file for package SFEcompiz-extra
#

%include Solaris.inc

Name:                    SFEcompiz-extra
Summary:                 Extra compiz plugin
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
Source0:		 http://www.anykeysoftware.co.uk/compiz/plugins/extra-plugins-0.5.0.2.tar.gz
URL:		         http://compiz.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Patch1:			 compiz-extra-01-solaris-port.diff

%package root

Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires:		 SUNWpostrun-root
Requires:		 SUNWgnome-config
BuildRequires:           SFEbcop

%prep
rm -rf %name-%version
mkdir %name-%version
%setup -c -n %name-%version
gtar -xzf %SOURCE0
cd extra-plugins-0.5.0
%patch1 -p1

%build
cd extra-plugins-0.5.0/
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

rm -r resize
rm *.sh
for plugin in `ls`
do
cd $plugin
if test "X$plugin" = "Xvignettes"; then
        CFLAGS="$RPM_OPT_FLAGS" \
        ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir} \
	--localstatedir=%{_localstatedir} \
	--disable-scrollkeeper
	make 
	cd ..
else
	if test -a $plugin.options; then
	   bcop -g $plugin.options
	fi
	if test "X$plugin" = "Xscreensaver"; then
	   MODE=noXExt make -j $CPUS DESTDIR=$RPM_BUILD_ROOT
	else
	   make -j $CPUS DESTDIR=$RPM_BUILD_ROOT
	fi
	cd ..
fi
done

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/gconf/schemas/
cd extra-plugins-0.5.0/
for plugin in `ls`
do
cd $plugin
if test "X$plugin" = "Xvignettes"; then
  make DESTDIR=$RPM_BUILD_ROOT install
else    
  make DESTDIR=$RPM_BUILD_ROOT/%{_libdir}/compiz IMAGEDIR=$RPM_BUILD_ROOT/%{_datadir}/compiz install
fi
if test -a $plugin.schema; then
  cp *.schema $RPM_BUILD_ROOT/%{_sysconfdir}/gconf/schemas/
fi
cd ..
done

rm $RPM_BUILD_ROOT/%{_libdir}/compiz/*.a 
rm $RPM_BUILD_ROOT/%{_libdir}/compiz/*.la

# fix file attribute problems
chmod 644 $RPM_BUILD_ROOT/%{_datadir}/compiz/*.png
chmod 644 $RPM_BUILD_ROOT/%{_sysconfdir}/gconf/schemas/*.schema

%clean
rm -rf $RPM_BUILD_ROOT

%post root
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/3d.schema 
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/animation.schema 
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/bench.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/bs.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/crashhandler.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/fakergb.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/flash.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/group.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/kiosk.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/mblur.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/mousegestures.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/neg.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/opacify.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/put.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/quickchange.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/reflex.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/ring.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/screensaver.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/showdesktop.schema 
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/snow.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/snap.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/splash.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/thumbnail.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/tile.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/trailfocus.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/wall.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/wallpaper.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/widget.schema
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/winrules.schema

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/compiz
%dir %attr (0755, root, bin) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/compiz
%{_datadir}/compiz/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/*.schema

%changelog
* Mon June 25 2007 - <erwann.chenede@sun.com>
- modification/polish for SFE integration
* Thu May 29 2007 - <chris.wang@sun.com>
- initial creation


