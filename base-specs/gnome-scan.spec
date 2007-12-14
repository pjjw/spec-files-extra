#
# spec file for package gnomescan
#
#
Name:         gnome-scan
License:      GPL
Group:        Applications/Multimedia
Version:      0.5.2
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      gnomescan - scanner client for the GNOME desktop
Source:	      http://download.gna.org/gnomescan/gnome-scan-%{version}.tar.gz
URL:          http://www.gnome.org/projects/gnome-scan/index
# date:2007-02-25 owner:xz159989 type:feature
Patch1:       gnome-scan-01-build.diff

%package devel
Summary:                 %{summary} - development files
Group:        System/GUI/GNOME
Requires:     %name 

%prep
%setup -q
%patch1 -p0

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

aclocal
libtoolize --force
glib-gettextize --force
autoconf -f
automake
./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info
	    		
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_libdir}/lib*.so*
%{_libdir}/pkgconfig/*
%{_libdir}/gimp
%{_datadir}/pixmaps/*
%{_datadir}/applications/*

%files devel
%defattr (-, root, root)
%{_includedir}/*
%{_datadir}/gtk-doc

%changelog
* Fri Dec 14 2007 - simon.zheng@sun.com
  Rework gnome-scan-01-build.diff.
* Sat Nov 17 2007 - daymobrew@users.sourceforge.net
- Bump to 0.5.2. Correct module name (gnome-scan) and update url. Disable
  obsolete patch, 01-build.
* Tue Mar 20 2007 - simon.zheng@sun.com
- initial version for pkgbuild
