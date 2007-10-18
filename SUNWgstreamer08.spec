#
# spec file for package gstreamer-0.8
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define         majmin          0.8

Name:           SUNWgstreamer08
Summary:	GStreamer streaming media framework runtime (API version 0.8)
License:        LGPL
Version:	%{majmin}.12

Source:		http://gstreamer.freedesktop.org/src/gstreamer/gstreamer-%{version}.tar.bz2
Patch1:         gstreamer08-01-gettext.diff

SUNW_BaseDir:   %{_prefix}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: CBEbison
BuildRequires: SUNWPython
BuildRequires: SUNWPython-extra
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWpng-devel
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
Requires: SUNWgnome-audio
Requires: SUNWgnome-config
Requires: SUNWgnome-vfs
Requires: SUNWlibms
Requires: SUNWperl584core
Requires: SUNWxorg-clientlibs
Requires: SUNWzlib
Requires: %{name}-root

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gstreamer-%{version}
%patch1 -p1

%build
# Need /usr/X11/lib and /usr/X11/include to gain access to libXv.so
# needed for xvimagesink.
#
export CFLAGS="%optflags -I/usr/sfw/include -I/usr/X11/include -DANSICPP"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib"

glib-gettextize -f
aclocal -I common/m4 $ACLOCAL_FLAGS
libtoolize --copy --force
autoheader
autoconf
automake -a -c -f
./configure \
  --prefix=%{_prefix} \
  --sysconfdir=%{_sysconfdir} \
  --mandir=%{_mandir}   \
  --enable-gtk-doc \
  --disable-plugin-builddir --disable-tests --disable-examples \
  --with-cachedir=%{_localstatedir}/cache/gstreamer-%{majmin}	\
  --enable-docs-build --disable-docbook --disable-static     	\
  --disable-rpath --enable-debug \
  --program-suffix=""
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/gstreamer-%{majmin}

rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majmin}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libgstmedia-info*.so.0.0.0

mkdir -p $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majmin}/tools

# remove tools, provided by the 0.10 version now
for a in launch inspect register xmllaunch complete compprep feedback md5sum typefind xmlinspect
do
  rm $RPM_BUILD_ROOT%{_bindir}/gst-$a
  mv $RPM_BUILD_ROOT%{_bindir}/gst-${a}-%{majmin} \
     $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majmin}/tools
done
rmdir $RPM_BUILD_ROOT%{_bindir}

perl -pi -e 's,^toolsdir=.*,toolsdir=\${exec_prefix}/lib/gstreamer-%{majmin}/tools,' $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gstreamer-%{majmin}.pc

rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/*.a
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgst*.so*
%{_libdir}/gstreamer-%{majmin}/lib*.so*
%{_libdir}/gstreamer-%{majmin}/tools
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_localstatedir}
%{_localstatedir}/cache/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/gstreamer-%{majmin}/gst
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon May 15 2006 - laca@sun.com
- fixed
- added patch gettext.diff to fix building l10n content
* Mon May 15 2006 - justin.conover@gmail.com
- Initial spec-file created
