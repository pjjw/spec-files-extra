#
# spec file for package SFElibcanberra
#
# includes module(s): libcanberra
#
%include Solaris.inc

Name:                    SFElibcanberra
Summary:                 Event Sound API Using XDG Sound Theming Specification
Version:                 0.8
License:                 LGPLv2.1
URL:                     http://0pointer.de/blog/projects/sixfold-announcement.html
Source:                  http://0pointer.de/lennart/projects/libcanberra/libcanberra-%{version}.tar.gz
Patch1:                  libcanberra-01-solaris.diff
Patch2:                  libcanberra-02-gstreamer.diff
Patch3:                  libcanberra-03-fix-gst-play.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFExdg-sound-theme
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-media
Requires: SUNWogg-vorbis
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWogg-vorbis-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libcanberra-%version
%patch1 -p1 
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

glib-gettextize -f
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la
rm $RPM_BUILD_ROOT%{_libdir}/libcanberra/*.a
rm $RPM_BUILD_ROOT%{_libdir}/libcanberra/*.la

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gtk-2.0
%{_libdir}/libcanberra
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%{_datadir}/gtk-doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/gnome

%changelog
* Fri Aug 29 2008 - brian.cameron@sun.com
- Add patch libcanberra-03-fix-gst-play so it actually plays the sound.
* Fri Aug 29 2008 - brian.cameron@sun.com
- Add patch libcanberra-02-gstreamer.diff to add audioconvert and audioresample
  plugins to the output pipeline, so it works on Solaris.
* Thu Aug 28 2008 - brian.cameron@sun.com
- Bump to 0.8.  Now has its own GStreamer support, so removed our patch.
* Wed Aug 20 2008 - brian.cameron@sun.com
- Add Requires/BuildRequires and patch libcanberra-02-gstreamer.diff to support
  a GStreamer backend.
* Thu Aug 14 2008 - brian.cameron@sun.com
- Created with version 0.6.
