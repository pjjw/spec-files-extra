#
# spec file for package SFEmplayer
#
# includes module(s): mplayer
#
%include Solaris.inc

%define codecdir %{_libdir}/mplayer/codecs

Name:                    SFEmplayer
Summary:                 mplayer - The Movie Player
Version:                 1.0
%define tarball_version 1.0rc1
Source:                  http://www.mplayerhq.hu/MPlayer/releases/MPlayer-%{tarball_version}.tar.bz2
Patch1:                  mplayer-01-cddb.diff
Patch2:                  mplayer-02-makefile-libfame-dep.diff
Patch3:                  mplayer-03-asmrules_20061231.diff
Patch4:                  mplayer-04-cabac-asm.diff
Source3:                 http://www.mplayerhq.hu/MPlayer/skins/Blue-1.7.tar.bz2
Source4:                 http://www.mplayerhq.hu/MPlayer/skins/Abyss-1.6.tar.bz2
Source5:                 http://www.mplayerhq.hu/MPlayer/skins/neutron-1.5.tar.bz2
Source6:                 http://www.mplayerhq.hu/MPlayer/skins/proton-1.2.tar.bz2
Source7:                 http://www.3gpp.org/ftp/Specs/latest/Rel-6/26_series/26104-610.zip
Source8:                 http://www.3gpp.org/ftp/Specs/latest/Rel-6/26_series/26204-600.zip
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
Requires: SUNWsmbau
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
%patch3 -p1
%patch4 -p1

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
export LDFLAGS="-L%{x11}/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib" 
export CC=gcc

bash ./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --confdir=%{_sysconfdir}         \
            --enable-gui                     \
            --enable-menu                    \
            --with-extraincdir=%{x11}/include  \
            --with-x11libdir=%{x11}/lib      \
            --with-extraincdir=/usr/sfw/include        \
            --with-extralibdir=/usr/sfw/lib            \
            --with-codecsdir=%{codecdir} \
            --enable-libfame                 \
            --enable-faad-external           \
            --enable-live                    \
            --with-livelibdir=/usr/lib/live  \
	    --enable-rpath		     \
            --enable-largefiles              \
            --disable-directfb

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mplayer/codecs
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
* Sun Apr 22 2007 - dougs@truemail.co.th
- Added /usr/gnu/libs to LDFLAGS
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires SUNWsmbau after check-deps.pl run.
* Sun Jan  7 2007 - laca@sun.com
- split the codecs out into SFEmplayer-codecs
* Wed Jan  3 2007 - laca@sun.com
- re-add patches cddb and makefile-libfame-dep after merging with 1.0rc1
- add patches asmrules_20061231 (fixes a buffer overflow) and
  cabac-asm (disables some asm stuff that doesn't seem to compile on Solaris.
* Wed Nov 29 2006 - laca@sun.com
- bump to 1.0rc1
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
