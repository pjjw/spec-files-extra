#
# spec file for package libtorrent
#
# includes module(s): libtorrent
#

Name:		libtorrent
Summary:	BitTorrent library written in C++
Version:	0.12.2
Source:		http://libtorrent.rakshasa.no/downloads/libtorrent-%{version}.tar.gz
Patch1:         libtorrent-01-madvise.diff
Patch2:         libtorrent-02-event-ports.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

aclocal -I ./scripts
autoheader
libtoolize --automake --copy --force
automake
autoconf
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_cxx_libdir}     \
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --enable-shared		\
	    --disable-static		\
	    --with-ports

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_cxx_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat May 24 2008 - trisk@acm.jhu.edu.
- Enable ports, add patch2
* Fri May  9 2008 - laca@sun.com
- Initial base spec file
