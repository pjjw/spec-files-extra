#
# spec file for package SFEvlc
#
# includes module(s): vlc
#
%include Solaris.inc

Name:                    SFEvlc
Summary:                 vlc - the cross-platform media player and streaming server
Version:                 0.8.6a
Source:                  http://download.videolan.org/pub/videolan/vlc/0.8.6a/vlc-%{version}.tar.bz2
Patch1:                  vlc-01-configure-no-pipe.diff
Patch2:                  vlc-02-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWhal
Requires: SUNWdbus
Requires: SFElibdvbpsi
Requires: SUNWlibcdio
Requires: SFElibmad
Requires: SFEffmpeg
Requires: SFEliba52
Requires: SFElibdts
Requires: SFEwxwidgets
BuildRequires: SUNWdbus-devel
BuildRequires: SFElibdvbpsi-devel
BuildRequires: SUNWlibcdio-devel
BuildRequires: SFElibmad-devel
BuildRequires: SFEffmpeg-devel
BuildRequires: SFEliba52-devel
BuildRequires: SFElibdts-devel
BuildRequires: SFEwxwidgets-devel


%prep
%setup -q -n vlc-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -D_XOPEN_SOURCE=500 -D__EXTENSIONS__"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

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

autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} --disable-libmpeg2
# Disable libmpeg2 to get past configure.

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%changelog
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
