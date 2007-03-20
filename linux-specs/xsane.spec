#
# spec file for package XSane 
#
Name:         xsane
License:      GPL
Group:        Applications/Multimedia
Version:      0.994
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      An X Window System front-end for the SANE scanner interface.
Source:       http://www.xsane.org/download/%{name}-%{version}.tar.gz
# date:2007-02-25 owner:xz159989 type:feature
Patch1:       xsane-01-gettext.diff
URL:          http://www.xsane.org/
Buildroot:    %{_tmppath}/%{name}-%{version}-buildroot

BuildPrereq: sane-backends-devel, gimp-devel
BuildPrereq: libpng-devel, libjpeg-devel
BuildRequires: desktop-file-utils >= 0.2.92

%description
XSane is an X based interface for the SANE (Scanner Access Now Easy)
library, which provides access to scanners, digital cameras, and other
capture devices. XSane is written in GTK+ and provides control for
performing the scan and then manipulating the captured image.

%prep
rm -rf %{buildroot}
%setup -q
%patch1 -p1

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

aclocal -I m4
libtoolize --force
glib-gettextize --force
autoconf -f
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
%ifos solaris
make -j$CPUS RANLIB=/usr/ccs/bin/ranlib
%else
make -j$CPUS
%endif

%install
rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT MKINSTALLDIRS=`pwd`/mkinstalldirs
rmdir $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_datadir}/sane
%{_libdir}/gimp/2.0/plug-ins/*
%{_mandir}/*/*

%changelog
* Tue Mar 20 2007 Simon Zheng <simon.zheng@sun.com>
- initial version for pkgbuild 
