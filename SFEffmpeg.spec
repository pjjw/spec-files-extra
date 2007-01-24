#
# spec file for package SFEffmpeg
#
# includes module(s): FFmpeg
#

%include Solaris.inc
Name:                    SFEffmpeg
Summary:                 FFmpeg - a very fast video and audio converter
%define year 2007
%define month  01
%define day    10
Version:                 %{year}.%{month}.%{day}
Source:                  http://pkgbuild.sf.net/spec-files-extra/tarballs/ffmpeg-export-%{year}-%{month}-%{day}.tar.bz2
Patch1:                  ffmpeg-01-BE_16.diff
SUNW_BaseDir:            %{_basedir}
URL:                     http://ffmpeg.mplayerhq.hu/index.html
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWmlib
Requires: SFEsdl
BuildRequires: SFEsdl-devel
Requires: SUNWxwrtl
Requires: SUNWzlib

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n ffmpeg-export-%{year}-%{month}-%{day}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="-O4"
export LDFLAGS="%_ldflags"
./configure \
    --prefix=%{_prefix} \
    --enable-sunmlib \
    --cc=gcc
make -j $CPUS
cd libpostproc
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# workaround for a bug in the 2007-01-10 snapshot: make install is
# looking for libpostproc.pc which doesn't exist
touch libpostproc.pc
cd libpostproc
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libpostproc.pc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
# could not build this project as a shared lib
%{_libdir}/lib*.a
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/vhook
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/ffmpeg
%{_includedir}/postproc

%changelog
* Sun Jan 21 2007 - laca@sun.com
- fix devel pkg default attributes
* Wed Jan 10 2007 - laca@sun.com
- create