#
# spec file for package SFEalsa-lib
#
# includes module(s): alsa-lib
#
%include Solaris.inc

Name:                    SFEalsa-lib
Summary:                 alsa-lib
Version:                 1.0.14a
Source:                  ftp://ftp.alsa-project.org/pub/lib/alsa-lib-%{version}.tar.bz2
Source1:		 byteswap-compat.h
Source2:		 endian-compat.h
Patch1:			 alsa-lib-01-configure.diff
Patch2:			 alsa-lib-02-byteorder.diff
Patch3:			 alsa-lib-03-alloca.diff
Patch4:			 alsa-lib-04-inttypes.diff
Patch5:			 alsa-lib-05-ioctl.diff
Patch6:			 alsa-lib-06-async.diff
Patch7:			 alsa-lib-07-aflocal.diff
Patch8:			 alsa-lib-08-mapfile.diff
Patch9:			 alsa-lib-09-search.diff
Patch10:		 alsa-lib-10-err.diff
Patch11:		 alsa-lib-11-sockio.diff
Patch12:		 alsa-lib-12-compat.diff
Patch13:		 alsa-lib-13-global.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n alsa-lib-%version
cp %{SOURCE1} include
cp %{SOURCE2} include
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# /usr/bin/sed is busted. Find a better one :)
export PATH=/usr/xpg4/bin:$PATH

CC=/usr/sfw/bin/gcc
export CPPFLAGS="-D_POSIX_SOURCE -D__EXTENSIONS__ -D_XPG4_2"
export CFLAGS="-O3"
export LDFLAGS="%_ldflags"
libtoolize -f -c
aclocal
autoheader
automake -f -a
autoconf -f
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
            --enable-shared			\
	    --disable-static			\
	    --without-versioned

gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/alsa-lib/*/*la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/alsa-lib
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/alsa

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Sun Aug 12 2007 - dougs@truemail.co.th
- Fixed headers for easier building of apps
* Sat Aug 11 2007 - dougs@truemail.co.th
- Initial version
