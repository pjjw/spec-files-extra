#
# spec file for package gegl
#
#
Name:         gegl
License:      LGPL
Group:        Applications/Multimedia
Version:      0.0.14
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GEGL (Generic Graphics Library) is a graph based image processing framework.
Source:	      ftp://ftp.gimp.org/pub/gegl/0.0/%{name}-%{version}.tar.bz2
URL:          http://www.gegl.org/
Patch1:	      gegl-01-build.diff

%package devel
Summary:      %{summary} - development files
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
- Initial version for pkgbuild.
  Add a patch gegl-01-build.diff.
