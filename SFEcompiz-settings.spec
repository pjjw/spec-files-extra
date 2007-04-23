#
# spec file for package SFEcompiz-settings
#

%include Solaris.inc

Name:                    SFEcompiz-settings
Summary:                 compiz-settings
Version:                 0.07
%define tarball_version 0.07-2
Source:			 http://www.gnome.org/~erwannc/compiz/compiz-settings_%{tarball_version}.tar.gz
Source1:		 http://www.gnome.org/~erwannc/compiz/jds-integration.tar.bz2
Patch1:			 compiz-settings-solaris.2-3-7.diff 
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:		 SFEcompiz
Requires: 		 SUNWgnome-base-libs
BuildRequires: 	 SUNWgnome-base-libs-devel

%prep
%setup -q -n compizsettings-trunk
%patch1 -p1
gtar fxvj %{SOURCE1}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="-lX11 -lXext"

aclocal
autoheader
automake -a -c -f
autoconf
 
./configure --prefix=%{_prefix}	\
			--bindir=%{_bindir}    \
			--datadir=%{_datadir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart
cp compiz-autostart.desktop $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart
cp compiz-autostart.sh run-compiz stop-compiz $RPM_BUILD_ROOT%{_bindir}
cp compiz.png $RPM_BUILD_ROOT%{_datadir}/pixmaps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/applications
%dir %attr(0755, root, other) %{_datadir}/pixmaps
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
#%dir %attr(0755, root, sys) %{_sysconfdir}/xdg
#%dir %attr(0755, root, sys) %{_sysconfdir}/xdg/autostart
%{_sysconfdir}/xdg/autostart/*

%changelog
* Mon Apr 23 2007 - Erwann Chenede <erwann at sun com>
- added Gnome integration scripts and icons
* Tue Mar 06 2007 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
