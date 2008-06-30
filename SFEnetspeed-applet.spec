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
Version:                 0.14
Source:                  http://www.wh-hms.uni-ulm.de/~mfcn/netspeed/packages/netspeed_applet-%{version}.tar.gz
Patch1:                  netspeedapplet-01-sockio.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}_%{version}-build
%include default-depend.inc

Requires:    SUNWgnome-libs
Requires:    SUNWgnome-panel
Requires:    SUNWlibgtop
BuildRequires:    SUNWgnome-libs-devel
BuildRequires:    SUNWgnome-panel-devel
BuildRequires:    SUNWlibgtop-devel

%prep
rm -rf %name_%version
%setup -q -n netspeed_applet-%version
%patch1 -p1 -b .patch01

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags"

glib-gettextize --force
aclocal
libtoolize --copy --force
intltoolize --force --copy --automake
automake -a -f
autoconf -f

./configure --prefix=%{_prefix}  \
            --libexecdir=%{_libexecdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755,root,sys) %{_datadir}
%{_datadir}/omf/
%{_datadir}/gnome/help/netspeed_applet
%{_datadir}/locale/
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/netspeed_applet
%{_datadir}/pixmaps/netspeed_applet.png


%changelog
* Mon Jun 30 2008 - Andras Barna (andras.barna@gmail.com)
- Fix permissions
* Thu Jun 23 2008 - Andras Barna (andras.barna@gmail.com)
- Initial spec
