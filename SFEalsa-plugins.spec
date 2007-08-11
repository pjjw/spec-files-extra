#
# spec file for package SFEalsa-plugins
#
# includes module(s): alsa-plugins
#
%include Solaris.inc

Name:                    SFEalsa-plugins
Summary:                 alsa-plugins
Version:                 1.0.14
Source:                  ftp://ftp.alsa-project.org/pub/plugins/alsa-plugins-%{version}.tar.bz2
Source1:		 asound.conf
Patch1:			 alsa-plugins-01-configure.diff
Patch2:			 alsa-plugins-02-oss.diff
Patch3:			 alsa-plugins-03-dsp.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: oss
BuildRequires: SUNWdbus-devel
Requires: SUNWdbus
BuildRequires: SUNWspeex-devel
Requires: SUNWspeex

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n alsa-plugins-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
	    --bindir=%{_bindir}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
            --enable-shared			\
	    --disable-static

gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/alsa-lib/*.la

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%config %{_sysconfdir}/asound.conf

%changelog
* Sun Aug 12 2007 - dougs@truemail.co.th
- Initial version
