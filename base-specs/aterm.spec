#
# spec file for package aterm.spec
#
# includes module(s): aterm
#
%include Solaris.inc

%define src_name	aterm
%define src_url		ftp://ftp.afterstep.org/apps/aterm

Name:                   aterm
Summary:                aterm terminal
Version:                1.0.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
SFWLIB="-L/usr/sfw/lib -R/usr/sfw/lib"
GNULIB="-L/usr/gnu/lib -R/usr/gnu/lib"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
cppflags="-I/usr/sfw/include/freetype2 -I/usr/gnu/include -I/usr/sfw/include -I/usr/X11/include"
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer $cppflags"
export LDFLAGS="%{_ldflags} $GNULIB $SFWLIB $X11LIB"
export LD_OPTIONS="$GNULIB $SFWLIB $X11LIB"
export CC=gcc

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --datadir=%{_datadir}		\
            --libexecdir=%{_libexecdir} 	\
            --sysconfdir=%{_sysconfdir} 	\
            --with-gtk				\
            --with-readline			\
            --disable-staticlibs		\
            --enable-sharedlibs

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%changelog
* Sat Apr 28 2007 - dougs@truemail.co.th
- Initial version
