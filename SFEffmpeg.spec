#
# spec file for package SFEffmpeg
#
# includes module(s): FFmpeg
#

%include Solaris.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    SFEffmpeg
Summary:                 FFmpeg - a very fast video and audio converter

%define year 2007
%define month  07
%define day    31

Version:                 %{year}.%{month}.%{day}
Source:                  http://pkgbuild.sf.net/spec-files-extra/tarballs/ffmpeg-export-%{year}-%{month}-%{day}.tar.bz2
Patch1:                  ffmpeg-01-BE_16.diff
Patch2:                  ffmpeg-02-configure.diff
SUNW_BaseDir:            %{_basedir}
URL:                     http://ffmpeg.mplayerhq.hu/index.html
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWmlib
Requires: SUNWxwrtl
Requires: SUNWzlib
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
BuildRequires: SFElibdts-devel
Requires: SFElibdts
BuildRequires: SFElibgsm-devel
Requires: SFElibgsm
BuildRequires: SFEliba52-devel
Requires: SFEliba52
BuildRequires: SFEliba52-devel
Requires: SFEliba52
BuildRequires: SFExvid-devel
Requires: SFExvid
BuildRequires: SFElibx264-devel
Requires: SFElibx264
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
BuildRequires: SFEamrnb-devel
Requires: SFEamrnb
BuildRequires: SFEamrwb-devel
Requires: SFEamrwb
BuildRequires: SFElame-devel
Requires: SFElame
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SUNWlibtheora-devel
Requires: SUNWlibtheora

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n ffmpeg-export-%{year}-%{month}-%{day}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="-O4"
export LDFLAGS="%_ldflags -lm"
bash ./configure	\
    --prefix=%{_prefix} \
    --enable-sunmlib	\
    --cc=gcc		\
    --enable-libgsm	\
    --enable-libxvid	\
    --enable-libx264	\
    --enable-gpl	\
    --enable-pp		\
    --enable-liba52	\
    --enable-liba52bin	\
    --enable-libfaad	\
    --enable-libfaadbin	\
    --enable-libogg	\
    --enable-libtheora	\
    --enable-libmp3lame	\
    --enable-pthreads	\
    --enable-libvorbis	\
    --enable-libamr-nb	\
    --enable-libamr-wb	\
    --enable-static	\
    --enable-shared

make -j $CPUS
cd libpostproc
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir $RPM_BUILD_ROOT%{_libdir}/ffmpeg
cp config.mak $RPM_BUILD_ROOT%{_libdir}/ffmpeg

cd libpostproc
make install DESTDIR=$RPM_BUILD_ROOT

# Create a ffmpeg.pc - Some apps need it
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/ffmpeg.pc << EOM
Name: ffmpeg
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include
Description: FFmpeg codec library
Version: 51.40.4
Requires:  libavcodec libpostproc libavutil libavformat libswscale x264 ogg theora vorbisenc vorbis dts
Conflicts:
EOM

mv $RPM_BUILD_ROOT%{_libdir}/lib*.*a $RPM_BUILD_ROOT%{_libdir}/ffmpeg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/vhook
%{_libdir}/ffmpeg
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/ffmpeg
%{_includedir}/postproc

%changelog
* Wed Aug  3 2007 - dougs@truemail.co.th
- Bumped export version
- Added codecs
- Created ffmpeg.pc
* Tue Jul 31 2007 - dougs@truemail.co.th
- Added SUNWlibsdl test. Otherwise require SFEsdl
* Sat Jul 14 2007 - dougs@truemail.co.th
- Build shared library
* Sun Jan 21 2007 - laca@sun.com
- fix devel pkg default attributes
* Wed Jan 10 2007 - laca@sun.com
- create
