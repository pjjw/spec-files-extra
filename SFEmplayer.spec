#
# spec file for package SFEmplayer
#
# includes module(s): mplayer
#
%include Solaris.inc

Name:                    SFEmplayer
Summary:                 mplayer - The Movie Player
Version:                 1.0
%define tarball_version 1.0pre8
Source:                  http://www.mplayerhq.hu/MPlayer/releases/MPlayer-%{tarball_version}.tar.bz2
Source2:                 http://www1.mplayerhq.hu/MPlayer/releases/codecs/essential-20060611.tar.bz2
Source3:                 http://www.mplayerhq.hu/MPlayer/skins/Blue-1.6.tar.bz2
Source4:                 http://www.mplayerhq.hu/MPlayer/skins/Abyss-1.6.tar.bz2
Source5:                 http://www.mplayerhq.hu/MPlayer/skins/neutron-1.5.tar.bz2
Source6:                 http://www.mplayerhq.hu/MPlayer/skins/proton-1.2.tar.bz2
Source7:                 http://www.3gpp.org/ftp/Specs/latest/Rel-6/26_series/26104-610.zip
Source8:                 http://www.3gpp.org/ftp/Specs/latest/Rel-6/26_series/26204-600.zip
Patch1:                  mplayer-01-cddb.diff
Patch2:                  mplayer-02-makefile-libfame-dep.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{tarball_version}-build
%include default-depend.inc
Requires: SFElibsndfile
Requires: SFElibfame
Requires: SFElibdvdplay
Requires: SFElibmad
Requires: SFEliba52
Requires: SFEliveMedia
Requires: SFElame
Requires: SFEtwolame
Requires: SFEfaad2
Requires: SFElibmpcdec
Requires: SFEsdl
Requires: SUNWsmbau
Requires: SUNWgnome-audio
Requires: SUNWxorg-clientlibs
Requires: SUNWxorg-mesa
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWspeex
Requires: SUNWjpg
Requires: SUNWpng
Requires: SUNWogg-vorbis
Requires: SUNWlibtheora
Requires: SUNWgccruntime
Requires: SUNWlibcdio
Requires: SUNWgnome-base-libs
BuildRequires: SFElibsndfile-devel
BuildRequires: SFElibfame-devel
BuildRequires: SFElibdvdplay-devel
BuildRequires: SFElibmad-devel
BuildRequires: SFEliba52-devel
BuildRequires: SFEliveMedia
BuildRequires: SFElame-devel
BuildRequires: SFEtwolame-devel
BuildRequires: SFEfaad2-devel
BuildRequires: SFElibmpcdec-devel
BuildRequires: SFEsdl-devel
BuildRequires: SUNWgnome-audio-devel

%define x11	/usr/openwin
%ifarch i386 amd64
%define x11	/usr/X11
%endif

%prep
%setup -q -n MPlayer-%tarball_version
%patch1 -p1
%patch2 -p1
unzip %SOURCE7
unzip 26104-610_ANSI_C_source_code.zip
mv c-code libavcodec/amr_float
unzip %SOURCE8
unzip 26204-600_ANSI-C_source_code.zip
mv c-code libavcodec/amrwb_float

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="-O2 -D__hidden=\"\""
export LDFLAGS="-L%{x11}/lib -L/usr/sfw/lib" 
export CC=gcc

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --confdir=%{_sysconfdir}         \
            --enable-gui                     \
            --enable-menu                    \
            --with-x11incdir=%{x11}/include  \
            --with-x11libdir=%{x11}/lib      \
            --with-extraincdir=/usr/sfw/include        \
            --with-extralibdir=/usr/sfw/lib            \
            --with-codecsdir=%{_libdir}/mplayer/codecs \
            --enable-libfame                 \
            --enable-external-faad           \
            --enable-live                    \
            --with-livelibdir=/usr/lib/live  \
	    --enable-rpath		     \
            --enable-largefiles

echo "#ifndef SOLARIS" >> config.h
echo "#define SOLARIS" >> config.h
echo "#endif" >> config.h
gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mplayer/codecs
( 
	cd $RPM_BUILD_ROOT%{_libdir}/mplayer/codecs
	gtar fxvj %SOURCE2
	mv essential-20060611/* .
	rmdir essential-20060611
)
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mplayer/skins
(
	cd $RPM_BUILD_ROOT%{_datadir}/mplayer/skins
	gtar fxj %SOURCE3
	gtar fxj %SOURCE4
	gtar fxj %SOURCE5
	gtar fxj %SOURCE6
	ln -s Blue default
)
ln -s /usr/openwin/lib/X11/fonts/TrueType/FreeSerif.ttf $RPM_BUILD_ROOT%{_datadir}/mplayer/subfont.ttf
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

#
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%{_datadir}/mplayer
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%changelog
* Tue Sep 26 2006 - halton.huo@sun.com
- Add Requires after check-deps.pl run
* Tue Sep 26 2006 - halton.huo@sun.com
- Bump Source4 to version 1.6
* Thu Jul 27 2006 - halton.huo@sun.com
- Bump Source3 to version 1.6
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEmplayer
- delete -share subpkg
- update file attributes
* Mon Jun 13 2006 - dougs@truemail.co.th
- Bumped version to 1.0pre8
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
