#
# spec file for package SFEalsa-utils
#
# includes module(s): alsa-utils
#
%include Solaris.inc

Name:                    SFEalsa-utils
Summary:                 alsa-utils
Version:                 1.0.14
Source:                  ftp://ftp.alsa-project.org/pub/utils/alsa-utils-%{version}.tar.bz2
Patch1:			 alsa-utils-01-endian.diff
Patch2:			 alsa-utils-02-configure.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEalsa-lib-devel
Requires: SFEalsa-lib

%prep
%setup -q -n alsa-utils-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

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
	    --sbindir=%{_sbindir}		\
	    --bindir=%{_bindir}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
            --enable-shared			\
	    --disable-static			\
	    --disable-alsamixer

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_sbindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/alsa
%{_datadir}/sounds
%{_mandir}

%changelog
* Sat Aug 11 2007 - dougs@truemail.co.th
- Initial version
