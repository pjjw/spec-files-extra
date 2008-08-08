#
# spec file for package gst-ffmpeg
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: trisk
#
Name:           gst-ffmpeg
License:        LGPL
Version:        0.10.4
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Group:          Libraries/Multimedia
Summary:        GStreamer Streaming-media framework plug-ins - FFmpeg.
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-ffmpeg/gst-ffmpeg-%{version}.tar.bz2
Patch1:         gst-ffmpeg-01-BE_16.diff 
Patch2:         gst-ffmpeg-02-ext-ffmpeg.diff
Patch3:         gst-ffmpeg-03-new-codec-ids.diff
Patch4:         gst-ffmpeg-04-av_picture_copy.diff
Patch5:         gst-ffmpeg-05-disable-aac.diff
Patch6:         gst-ffmpeg-06-disable-mpegts.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Docdir:         %{_defaultdocdir}/doc
Autoreqprov:    on

%define 	majorminor	0.10

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

%prep
%setup -n gst-ffmpeg-%{version} -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
#CC=/usr/sfw/bin/gcc ; export CC ; \
#CFLAGS="%gcc_optflags -fno-rename-registers -fno-PIC -UPIC -mpreferred-stack-boundary=4"; export CFLAGS ; \
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; \
glib-gettextize -f
aclocal -I ./common/m4 $ACLOCAL_FLAGS
libtoolize --copy --force
intltoolize --copy --force --automake
autoheader
autoconf
automake -a -c -f
bash ./configure \
  --prefix=%{_prefix}	\
  --sysconfdir=%{_sysconfdir} \
  --mandir=%{_mandir}   \
  %{arch_opt}	\
  %{gtk_doc_option}	\
  --with-system-ffmpeg --with-check=no

# FIXME: hack: -mimpure-text is needed for linking non-PIC code
perl -pi -e 's/-shared /-shared -mimpure-text /' libtool
# FIXME: hack: stop the build from looping
touch po/stamp-it

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make 
else
  make
fi

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ]
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# Clean out files that should not be part of the rpm.
# This is the recommended way of dealing with it for RH8
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING README REQUIREMENTS
%{_libdir}/gstreamer-*/*.so
%{_sysconfdir}/gconf/schemas/gstreamer-*.schemas
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%post 
%{_bindir}/gst-register > /dev/null 2> /dev/null
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gstreamer-0.10.schemas"
for S in $SCHEMAS; do
 gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%package devel
Summary: 	GStreamer Plugin Library Headers.
Group: 		Development/Libraries
Requires: 	gstreamer-plugins-devel >= 0.10.0
Requires:       %{name} = %{version}

%description devel
GStreamer support libraries header files.

%files devel
%defattr(-, root, root)
%{_datadir}/gtk-doc

%changelog
* Wed Jul 23 2008 - trisk@acm.jhu.edu
- Add patch3, patch4, patch5, patch6 from Debian
* Tue Jul 22 2008 - trisk@acm.jhu.edu
- Update to 0.10.4, use external ffmpeg
* Thu Oct 18 2007 - trisk@acm.jhu.edu
- Initial spec, based on gst-plugins-good
