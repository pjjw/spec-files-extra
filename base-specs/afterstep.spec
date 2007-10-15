#
# spec file for package afterstep.spec
#
# includes module(s): afterstep
#
%include Solaris.inc

%define src_name	AfterStep
%define src_url		ftp://ftp.afterstep.org/stable

Name:                   afterstep
Summary:                afterstep window manager
Version:                2.2.5
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:			afterstep-01-lX11.diff
Patch2:			afterstep-02-sharedlib.diff
Patch3:			afterstep-03-typo.diff
Patch4:			afterstep-04-debug.diff

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

find . \( -name \*.c -o -name \*.h \) -print | while read i ; do
    dos2unix $i $i
done

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
GNULIB="-L/usr/gnu/lib -R/usr/gnu/lib"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
cppflags="-I/usr/gnu/include -I/usr/X11/include"
export CFLAGS="-g -O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer $cppflags"
export LD_OPTIONS="$GNULIB $X11LIB"
export LDFLAGS="$GNULIB $X11LIB"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --datadir=%{_datadir}		\
            --libexecdir=%{_libexecdir} 	\
            --sysconfdir=%{_sysconfdir} 	\
	    --disable-sigsegv			\
            --enable-staticlibs			\
	    --disable-sharedlibs

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%changelog
* Sat Apr 28 2007 - dougs@truemail.co.th
- Initial version
