#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define kde_version 3.5.8

Name:                SFEkdemultimedia3
Summary:             A collection of audio/video applications for KDE
Version:             %{kde_version}
Source:              http://mirrors.isc.org/pub/kde/stable/%{kde_version}/src/kdemultimedia-%{version}.tar.bz2
Patch1:              kdemultimedia-01-mpeglib.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# This also brings in all relevenat deps including kdelibs, qt, aRts and others.
Requires: SFEkdebase3
BuildRequires: SFEkdebase3-devel
Requires: SFEgraphviz
Requires: SFElibcdio
BuildRequires: SFElibcdio-devel
Requires: SUNWgnome-audio
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SFElame-devel
Requires: SFEtaglib
BuildRequires: SFEtaglib-devel
Requires: SFEakode
BuildRequires: SFEakode-devel
BuildRequires: SFEakode-encumbered
Requires: SUNWogg-vorbis
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWlibtheora
BuildRequires: SUNWlibtheora-devel
Requires: SUNWflac
BuildRequires: SUNWflac-devel
Requires: SFElibtunepimp
BuildRequires: SFElibtunepimp-devel
BuildRequires: SFElibtunepimp-encumbered
BuildRequires: oss

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEkdebase3-devel
Requires: SFElibcdio-devel
Requires: SUNWgnome-audio-devel
Requires: SFEtaglib-devel
Requires: SFEakode-devel
Requires: SUNWogg-vorbis-devel
Requires: SUNWlibtheora-devel
Requires: SUNWflac-devel
Requires: SFElibtunepimp-devel
Requires: oss

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SFEkdelibs3-root

%package encumbered
Summary:        %{summary} - support for encumbered codecs
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n kdemultimedia-%version
%patch1 -p1

if [ "x`basename $CC`" != xgcc ]
then
	%error This spec file requires Gcc, set the CC and CXX env variables
fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -fPIC -I/usr/X11/include -I/usr/gnu/include -I/usr/gnu/include/sasl -I/usr/sfw/include -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__ -fPIC -DPIC"

export CXXFLAGS="%cxx_optflags -I/usr/X11/include -I/usr/gnu/include -I/usr/gnu/include/sasl -I/usr/sfw/include -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__ -fPIC -DPIC"

export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -lc -lsocket -lnsl `/usr/bin/libart2-config --libs` -lartsflow -lartsflow_idl -lkmedia2 -lkmedia2_idl"

export LIBS=$LDFLAGS

export PATH="${PATH}:/usr/openwin/bin"

./configure -prefix %{_prefix} \
           --sysconfdir %{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --enable-final \
           --with-extra-includes="/usr/X11/include:/usr/gnu/include:/usr/gnu/include/sasl:/usr/sfw/include:/usr/include/pcre"


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/kapplications-merged
(cd $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/kapplications-merged; \
    ln -s ../applications-merged/kde-multimedia-music.menu)

# Build a partial file list leaving out encumbered pieces for the
# encumbered add-on package.
#
export EPATT="mp3|mpeg|mpc|MP3|mpg123|MPEG|MPC|m3u"
echo "%dir %attr (0755, root, bin) %{_libdir}" > \
    %{_builddir}/kdemultimedia-%version/flst
(cd ${RPM_BUILD_ROOT}; \
    find ./%{_libdir}/lib*.so* ./%{_libdir}/lib*.la* | \
    egrep -v "$EPATT" | \
    sed 's/^\.\//%attr (-, root, bin) /' >> \
    %{_builddir}/kdemultimedia-%version/flst)

echo "%dir %attr (0755, root, other) %{_libdir}/kde3" >> \
    %{_builddir}/kdemultimedia-%version/flst
(cd ${RPM_BUILD_ROOT}; \
    find ./%{_libdir}/kde3/* | \
    egrep -v "$EPATT" | \
    sed 's/^\.\//%attr (-, root, bin) /' >> \
    %{_builddir}/kdemultimedia-%version/flst)

echo "%dir %attr (0755, root, other) %{_libdir}/mcop" >> \
    %{_builddir}/kdemultimedia-%version/flst
echo "%dir %attr (0755, root, other) %{_libdir}/mcop/Arts" >> \
    %{_builddir}/kdemultimedia-%version/flst
echo "%dir %attr (0755, root, other) %{_libdir}/mcop/Arts/Environment" >> \
    %{_builddir}/kdemultimedia-%version/flst
echo "%dir %attr (0755, root, other) %{_libdir}/mcop/Noatun" >> \
    %{_builddir}/kdemultimedia-%version/flst
(cd ${RPM_BUILD_ROOT}; \
    find ./%{_libdir}/mcop/* -type f | \
    egrep -v "$EPATT" | \
    sed 's/^\.\//%attr (-, root, bin) /' >> \
    %{_builddir}/kdemultimedia-%version/flst)

echo "%dir %attr (0755, root, other) %{_datadir}/services" >> \
    %{_builddir}/kdemultimedia-%version/flst
(cd ${RPM_BUILD_ROOT}; \
    find ./%{_datadir}/services/* | \
    egrep -v "$EPATT" | \
    sed 's/^\.\//%attr (-, root, other) /' >> \
    %{_builddir}/kdemultimedia-%version/flst)

echo "%dir %attr (0755, root, bin) %{_includedir}" > \
    %{_builddir}/kdemultimedia-%version/flst-devel
echo "%dir %attr (0755, root, bin) %{_includedir}/arts" >> \
    %{_builddir}/kdemultimedia-%version/flst-devel
echo "%dir %attr (0755, root, bin) %{_includedir}/noatun" >> \
    %{_builddir}/kdemultimedia-%version/flst-devel
echo "%dir %attr (0755, root, bin) %{_includedir}/libkcddb" >> \
    %{_builddir}/kdemultimedia-%version/flst-devel
(cd ${RPM_BUILD_ROOT}; \
    find ./%{_includedir}/* -type f | \
    egrep -v "$EPATT" | \
    sed 's/^\.\//%attr (-, root, bin) /' >> \
    %{_builddir}/kdemultimedia-%version/flst-devel)

# KDE requires the .la files

%clean
rm -rf $RPM_BUILD_ROOT

%files -f flst
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/mimelnk
%{_datadir}/mimelnk/*
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*
%dir %attr (0755, root, other) %{_datadir}/servicetypes
%{_datadir}/servicetypes/*
%dir %attr (0755, root, sys) %{_datadir}/autostart
%{_datadir}/autostart/*

%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_datadir}/desktop-directories
%{_datadir}/desktop-directories/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*

%files devel -f flst-devel
%defattr (-, root, bin)

%files encumbered
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*mpeg*
%{_libdir}/*mpg*
%dir %attr (0755, root, other) %{_libdir}/kde3
%{_libdir}/kde3/*mp3*
%{_libdir}/kde3/*mpeg*
%{_libdir}/kde3/*mpc*
%{_libdir}/kde3/*m3u*
%dir %attr (0755, root, other) %{_libdir}/mcop
%{_libdir}/mcop/*mpg*
%{_libdir}/mcop/*MP3*
%{_libdir}/mcop/*MPC*
%{_libdir}/mcop/*MPEG*
%dir %attr (0755, root, other) %{_libdir}/mcop/Arts
%{_libdir}/mcop/Arts/*mpg*
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/mpeglib
%{_includedir}/mpeglib/*
%dir %attr (0755, root, bin) %{_includedir}/mpeglib_artsplug
%{_includedir}/mpeglib_artsplug/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/services
%{_datadir}/services/*m3u*
%{_datadir}/services/*mpc*
%{_datadir}/services/*mp3*
%{_datadir}/services/*mpeg*


%changelog
* Sun Jan 20 2008 - moinak.ghosh@sun.com
- Add dependencies to devel package. Added oss dependency.
* Sat Jan 19 2008 - moinak.ghosh@sun.com
- Initial spec.
