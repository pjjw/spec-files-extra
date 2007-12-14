#
# spec file for package babl
#
#
Name:         babl
License:      LGPL
Group:        Applications/Multimedia
Version:      0.0.16
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Babl is a dynamic, any to any, pixel format conversion library.
Source:	      ftp://ftp.gtk.org/pub/babl/0.0/%{name}-%{version}.tar.bz2
URL:          http://www.gegl.org/babl/
Patch1:       babl-01-build.diff

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
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_libdir}/lib*.so*
%{_libdir}/babl-0.0/*.so*
%{_libdir}/pkgconfig/*

%files devel
%defattr (-, root, root)
%{_includedir}/babl-0.0/babl/*

%changelog
* Fri Dec 14 2007 - simon.zheng@sun.com
- Initial version for pkgbuild.
  Add a patch babl-01-build.diff.
