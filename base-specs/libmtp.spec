#
# spec file for package libmtp
#
# includes module(s): libmtp
#

%define src_ver 0.2.4
%define src_name libmtp
%define src_url http://jaist.dl.sourceforge.net/sourceforge/%{src_name}

Name:		libmtp
Summary:	Implementation of Microsoft's Media Transfer Protocol (MTP)
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libmtp-01-wall.diff
Patch2:		libmtp-02-u_int.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    SFWLIB="-L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}"
else
    SFWLIB="-L/usr/sfw/lib -R/usr/sfw/lib"
fi

export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags $SFWLIB"

libtoolize -f -c
aclocal -I m4
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
rm -f $RPM_BUILD_ROOT%{_libdir}/libmtp/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Dec 30 2007 - markwright@internode.on.net
- Bump to 0.2.4
* Tue Sep 18 2007 - dougs@truemail.co.th
- Initial base spec file
