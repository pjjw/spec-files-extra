#
# spec file for package dvgrab
#
# includes module(s): dvgrab
#

%define src_ver 3.0
%define src_name dvgrab
%define src_url http://%{sf_mirror}/sourceforge/kino

Name:		dvgrab
Summary:	DV grabbing utility
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Source1:        byteswap-compat.h
Source2:        endian-compat.h
Patch1:		dvgrab-01-configure.diff
Patch2:		dvgrab-02-v4l2.diff
Patch3:		dvgrab-03-u_int.diff
Patch4:		dvgrab-04-sunpro.diff
Patch5:		dvgrab-05-strsep.diff
Patch6:		dvgrab-06-return.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
#%patch4 -p1
%patch5 -p1
%patch6 -p1
cp %SOURCE1 byteswap.h
cp %SOURCE2 endian.h

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-D__ASSERT_FUNCTION=__FUNCTION__"
export CC=gcc
export CFLAGS="-O4 -fPIC"
export CXX=g++
export CXXFLAGS="-O4 -fPIC"
export LDFLAGS="%_ldflags"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export CFLAGS="$CFLAGS -m64"
        export CXXFLAGS="$CXXFLAGS -m64"
        export LDFLAGS="-Wl,-64 -L%{_libdir} -R%{_libdir} $LDFLAGS"
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
