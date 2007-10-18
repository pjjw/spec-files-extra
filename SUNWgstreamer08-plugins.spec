#
# spec file for package gstreamer-plugins-0.8
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define         majmin          0.8

Name:           SUNWgstreamer08-plugins
Summary:	GStreamer streaming media framework plugins (API version 0.8)
License:        LGPL
Version:	%{majmin}.12

Source:		http://gstreamer.freedesktop.org/src/gst-plugins/gst-plugins-%{version}.tar.bz2
Patch1:         gst-plugins08-01-gettext.diff

SUNW_BaseDir:            %{_prefix}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgstreamer08-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: CBEbison
BuildRequires: SUNWPython
BuildRequires: SUNWmusicbrainz-devel
BuildRequires: SUNWspeex-devel
BuildRequires: SUNWflac-devel
BuildRequires: SUNWlibtheora-devel
BuildRequires: SUNWogg-vorbis-devel
BuildRequires: SUNWPython-extra
BuildRequires: SUNWliboil-devel
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWpng-devel
BuildRequires: SUNWlibcdio-devel
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWmusicbrainz
Requires: SUNWspeex
Requires: SUNWflac
Requires: SUNWlibtheora
Requires: SUNWogg-vorbis
Requires: SUNWliboil
Requires: SUNWlibms
Requires: SUNWgnome-audio
Requires: SUNWgnome-config
Requires: SUNWgnome-vfs
Requires: SUNWjpg
Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWperl584core
Requires: SUNWpng
Requires: SUNWzlib
Requires: SFElibcdio
Requires: %{name}-root
Requires: SUNWpostrun
Requires: SUNWgstreamer08

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun
Requires: SUNWgnome-config

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
%setup -q -n gst-plugins-%{version}
%patch1 -p1

%build
# Need /usr/X11/lib and /usr/X11/include to gain access to libXv.so
# needed for xvimagesink.
#
export CFLAGS="%optflags -I/usr/sfw/include -I/usr/X11/include -DANSICPP"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib"
export PATH=%{_libdir}/gstreamer-%{majmin}/tools:$PATH

glib-gettextize -f
aclocal -I ./m4 -I ./common/m4 $ACLOCAL_FLAGS
libtoolize --copy --force
autoheader
autoconf
automake -a -c -f
./configure \
  --prefix=%{_prefix} \
  --sysconfdir=%{_sysconfdir}   \
  --mandir=%{_mandir}   \
  --enable-external   	\
  --with-plugins="adder,alpha,audioconvert,audioscale,audiorate,auparse,avi,chart,colorspace,cutter,debug,deinterlace,effectv,festival,ffmpegcolorspace,filter,flx,goom,interleave,law,level,matroska,median,mixmatrix,multifilesink,multipart,overlay,passthrough,playback,playondemand,silence,sine,smooth,smpte,spectrum,speed,stereo,switch,tags,tcp,typefind,udp,videobox,videocrop,videodrop,videoflip,videofilter,videomixer,videorate,videoscale,videotestsrc,volenv,volume,wavenc,wavparse" \
  --disable-aalib       \
  --disable-cdparanoia  \
  --disable-divx        \
  --disable-dts         \
  --disable-dxr3        \
  --disable-shout       \
  --disable-jack        \
  --disable-mikmod      \
  --disable-mplex       \
  --disable-sidplay     \
  --disable-musicbrainz \
  --disable-xine        \
  --disable-a52dec      \
  --disable-dirac       \
  --disable-libdv       \
  --disable-dvdnav      \
  --disable-dvdread     \
  --disable-faad        \
  --disable-libfame     \
  --disable-gsm         \
  --disable-lame        \
  --disable-mad         \
  --disable-mpeg2dec    \
  --disable-mpeg2enc    \
  --disable-swfdec      \
  --disable-tarkin      \
  --disable-xvid 
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_bindir}/gst-visualise-%{majmin}
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majmin}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majmin}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majmin}/libgstvideo4linux2.so

mkdir -p $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majmin}/tools
mv $RPM_BUILD_ROOT%{_bindir}/gst-launch-ext-%{majmin} \
   $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majmin}/tools
rmdir $RPM_BUILD_ROOT%{_bindir}

rm -rf $RPM_BUILD_ROOT%{_mandir}/man1/gst-visualise-%{majmin}.1

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z][a-z]
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z][a-z]-[A-Z][A-Z]
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x %{_libdir}/gstreamer-%{majmin}/tools/gst-register-%{majmin} || exit 1'  
  echo '%{_libdir}/gstreamer-%{majmin}/tools/gst-register-%{majmin} 2>&1'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b

%postun
( echo 'test -x %{_libdir}/gstreamer-%{majmin}/tools/gst-register-%{majmin} || exit 1'  
  echo '%{_libdir}/gstreamer-%{majmin}/tools/gst-register-%{majmin} 2>&1'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b

%post root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo '/usr/bin/gconftool-2 --makefile-install-rule $SDIR/gstreamer-0.8.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -i -c JDS_wait

%preun root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo '/usr/bin/gconftool-2 --makefile-uninstall-rule $SDIR/gstreamer-0.8.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -i -c SFE

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
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gstreamer-0.8.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/gstreamer-%{majmin}/gst

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%endif

%changelog
* Mon Jan 17 2007 - daymobrew@users.sourceforge.net
- Added code to %install to delete l10n files when not doing l10n build.
* Fri Jun  2 2006 - laca@sun.com
- use post/postun scripts to install schemas into the merged gconf files
* Mon May 15 2006 - laca@sun.com
- Initial spec file created
