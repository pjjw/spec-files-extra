#
# spec file for packages SUNWgnome-media-extras
#
# includes module(s): gst, gst-plugins-base, gst-plugins-good
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: your mom
#
%include Solaris.inc

%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)
%define SUNWlibsdl %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

%use gst_plugins_ugly = gst-plugins-ugly.spec
%use gst_plugins_bad = gst-plugins-bad.spec

%define gst_minmaj 0.10

Name:                    SFEgnome-media-extras
Summary:                 GNOME streaming media framework - extra plugins
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: CBEbison
BuildRequires: SUNWPython
BuildRequires: SUNWmusicbrainz-devel
BuildRequires: SFEfaad2-devel
BuildRequires: SFEliba52-devel
BuildRequires: SFElibmad-devel
BuildRequires: SFElibmpeg2-devel
BuildRequires: SFElibgsm-devel
BuildRequires: SFElibmpcdec-devel
BuildRequires: SFExvid-devel
BuildRequires: SFEamrnb-devel
BuildRequires: SFElibsndfile-devel
BuildRequires: SFElibid3tag-devel
BuildRequires: SUNWPython-extra
BuildRequires: SUNWliboil-devel
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SFElibdvdread-devel
BuildRequires: SUNWbzip
BuildRequires: SFEneon
BuildRequires: SUNWxorg-mesa
%if %SUNWlibsdl
BuildRequires:  SUNWlibsdl-devel
%else
BuildRequires:  SFEsdl-devel
%endif

Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-media-root
Requires: SUNWmusicbrainz
Requires: SUNWliboil
Requires: SUNWlibms
Requires: SUNWgnome-audio
Requires: SUNWgnome-config
Requires: SUNWgnome-vfs
Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWxorg-clientlibs
Requires: SUNWzlib
Requires: SFEneon
%if %with_hal
Requires: SUNWhal
%endif


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun-root
Requires: SUNWgnome-config

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%gst_plugins_ugly.prep -d %name-%version
%gst_plugins_bad.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
# Note that including  __STDC_VERSION n CFLAGS for gnome-media breaks the S9
# build for gstreamer,  gst-plugins, and gnome-media, so not including for them.
#
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export LDFLAGS="%_ldflags"

%gst_plugins_ugly.build -d %name-%version

export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
# gstmodplug needs C99 __func__
export CXXFLAGS="%cxx_optflags -features=extensions -I/usr/sfw/include"
export LDFLAGS="%_ldflags"

%gst_plugins_bad.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%gst_plugins_ugly.install -d %name-%version
%gst_plugins_bad.install -d %name-%version

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_minmaj}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_minmaj}/*.a
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif

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
%{_libdir}/gstreamer-%{gst_minmaj}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/gstreamer-%{gst_minmaj}/gst
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Change SUNWneon dependency to SFEneon.
* Wed Oct 17 2007 - trisk@acm.jhu.edu
- Initial spec, based on SUNWgnome-media
