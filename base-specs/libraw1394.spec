#
# spec file for package libraw1394
#
# includes module(s): libraw1394
#

%define src_ver 1.2.1
%define src_name libraw1394
%define src_url http://www.linux1394.org/dl

Name:		libraw1394
Summary:	Interface to IEEE-1394 subsystem
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Source1:	byteswap-compat.h
Source2:	endian-compat.h
Patch1:		libraw1394-01-solaris.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

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
rm -f $RPM_BUILD_ROOT%{_libdir}/libraw1394/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Oct  3 2007 - Doug Scott
- Updates from cvsdude
* Wed Oct  3 2007 - Doug Scott
- Updates from cvsdude
* Tue Sep  4 2007 - dougs@truemail.co.th
- Initial base spec file
