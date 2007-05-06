#
# spec file for package libggiwmh.spec
#
# includes module(s): libggiwmh
#

%define src_name        libggiwmh
%define src_url         http://www.ggi-project.org/ftp/ggi/v2.2

Name:                   libggiwmh
Summary:                Window Manager Hints for GGI
Version:                0.3.2
Source:                 %{src_url}/%{src_name}-%{version}.src.tar.bz2

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./autogen.sh
X11LIBS="-L/usr/X11/lib -R/usr/X11/lib"
PROTOINC=$RPM_BUILD_ROOT%{_includedir}
PROTOLIB=$RPM_BUILD_ROOT%{_libdir}
export CPPFLAGS="-I/usr/X11/include -I$PROTOINC"
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O4 -fno-omit-frame-pointer $CPPFLAGS"
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-i $X11LIBS -L$PROTOLIB"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
