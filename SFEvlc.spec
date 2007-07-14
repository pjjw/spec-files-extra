#
# spec file for package SFEvlc
#
# includes module(s): vlc
#
%include Solaris.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

%define	src_name	vlc
%define	src_url		http://download.videolan.org/pub/videolan/vlc

Name:                   SFEvlc
Summary:                vlc - the cross-platform media player and streaming server
Version:                0.8.6c
Source:                 %{src_url}/%{version}/%{src_name}-%{version}.tar.bz2
Patch1:                 vlc-01-configure-no-pipe.diff
Patch2:                 vlc-02-solaris.diff
Patch3:                 vlc-03-oss.diff
Patch4:                 vlc-04-solaris_specific.diff
Patch5:                 vlc-05-solaris-cmds.diff
Patch6:                 vlc-06-intl.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %SUNWlibsdl
BuildRequires:  SUNWlibsdl-devel
Requires:       SUNWlibsdl
%else
BuildRequires:  SFEsdl-devel
Requires:       SFEsdl
%endif
BuildRequires:  SFEsdl-image-devel
Requires:       SFEsdl-image
Requires:       SUNWhal
BuildRequires:  SUNWdbus-devel
Requires:       SUNWdbus
Requires:       SUNWxorg-clientlibs
BuildRequires:  SUNWsmbau
BuildRequires:  SFElibfribidi-devel
Requires:       SFElibfribidi
BuildRequires:  SFEfreetype-devel
Requires:       SFEfreetype
BuildRequires:  SFEliba52-devel
Requires:       SFEliba52
BuildRequires:  SFEffmpeg-devel
Requires:       SFEffmpeg
BuildRequires:  SFElibmad-devel
Requires:       SFElibmad
BuildRequires:  SFElibmpcdec-devel
Requires:       SFElibmpcdec
BuildRequires:  SFElibmatroska-devel
Requires:       SFElibmatroska
BuildRequires:  SUNWogg-vorbis-devel
Requires:       SUNWogg-vorbis
BuildRequires:  SFElibdvbpsi-devel
Requires:       SFElibdvbpsi
BuildRequires:  SFElibdvdread-devel
Requires:       SFElibdvdread
BuildRequires:  SFElibdvdread-devel
Requires:       SFElibdvdread
BuildRequires:  SFElibdts-devel
BuildRequires:  SFElibcddb-devel
Requires:       SFElibcddb
BuildRequires:  SFElibmpeg2-devel
Requires:       SFElibmpeg2
BuildRequires:  SFEvcdimager-devel
Requires:       SFEvcdimager

%prep
%setup -q -n vlc-%version
#%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
# ffmpeg is build with g++, therefore we need to build with g++

X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
GNULIB="-L/usr/gnu/lib -R/usr/gnu/lib"

export PATH=/usr/gnu/bin:$PATH
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
export CC=gcc
export CXX=g++
export CPPFLAGS="-D_XOPEN_SOURCE=500 -D__EXTENSIONS__ -I/usr/X11/include -I/usr/gnu/include"
export CFLAGS="-O4"
export LDFLAGS="$X11LIB $GNULIB"

# See: http://forum.videolan.org/viewtopic.php?t=15444
# Uses configure options:
# ./configure --enable-x11 --enable-opengl --enable-xvideo --disable-gtk
#  --enable-sdl --enable-ffmpeg --with-ffmpeg-mp3lame --enable-mad
#  --enable-libdvbpsi --enable-a52 --enable-dts --enable-libmpeg2
#  --enable-dvdnav --enable-faad --enable-vorbis --enable-ogg --enable-theora
#  --enable-faac --enable-mkv --enable-freetype --enable-fribidi --enable-speex
#  --enable-flac --enable-caca --enable-skins --disable-skins2 --disable-kde
#  --disable-qt --enable-wxwindows --enable-ncurses --enable-release
#  --with-a52-tree=/export/home/barts/liba52/a52dec-0.7.4 

rm ./configure
./bootstrap
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
	    --enable-shared			\
	    --disable-static

# Disable libmpeg2 to get past configure.

printf '%%%s/\/intl\/libintl.a/-lintl/\nwq\n' | ex - vlc-config

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vlc
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.a
%{_libdir}/vlc
%defattr (-, root, other)
%{_datadir}/locale

%changelog
* Sat Jul 14 2007 - dougs@truemail.co.th
- Build with gcc
* Fri Mar 23 2007 - daymobrew@users.sourceforge.net
- Add two patches, 01-configure-no-pipe and 02-solaris. Add multiple
  dependencies. Getting closer but not quite building yet.
  Patch 01-configure-no-pipe removes the '-pipe' test. It causes problems later
  with -DSYS_SOLARIS being added after -pipe and being rejected by the linker.
  Patch 02-solaris.diff fixes two compiler issues. First involves expansion of
  ?: code; second changes AF_LOCAL to AF_UNIX as the former is not defined in
  <sys/socket.h>.

* Thu Mar 22 2007 - daymobrew@users.sourceforge.net
- Initial version
