#
# spec file for package kino
#
# includes module(s): kino
#

%define src_ver 1.1.1
%define src_name kino
%define src_url http://dl.sourceforge.net/sourceforge/kino

Name:		kino
Summary:	DV editing utility
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Source1:        byteswap-compat.h
Source2:        endian-compat.h
Patch1:		kino-01-configure.diff
Patch2:		kino-02-u_int.diff
Patch3:		kino-03-oss.diff
Patch4:		kino-04-v4l.diff
Patch5:		kino-05-headers.diff
Patch6:		kino-06-tar.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
cp %SOURCE1 src/byteswap.h
cp %SOURCE2 src/endian.h

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PATH=/opt/jdsbld/bin:/usr/xpg4/bin:$PATH
export CPPFLAGS="-DNAME_MAX=14 -D__ASSERT_FUNCTION=__FUNCTION__ -I/usr/X11/include"
export CC=gcc
export CFLAGS="-O4 -fPIC"
export CXX=g++
export CXXFLAGS="-O4 -fPIC"
export LDFLAGS="%_ldflags"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export CFLAGS="$CFLAGS -m64"
        export CXXFLAGS="$CXXFLAGS -m64"
        export LDFLAGS="-Wl,-64 -L%{_libdir} -R%{_libdir} $LDFLAGS"
else
	export LDFLAGS="-L/usr/X11/lib -R/usr/X11/lib"
fi


libtoolize -f -c
aclocal
autoheader
autoconf -f
automake -a -f

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --enable-shared		\
	    --disable-static

#perl -pi -e 's,-shared,-Wl,-G' libtool
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Sep  4 2007 - dougs@truemail.co.th
- Initial base spec file
