#
# spec file for package libiec61883
#
# includes module(s): libiec61883
#

%define src_ver 1.1.0
%define src_name libiec61883
%define src_url http://www.linux1394.org/dl

Name:		libiec61883
Summary:	Streaming library for IEEE1394
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Source1:	byteswap-compat.h
Source2:	endian-compat.h
Patch1:		libiec61883-01-function.diff
Patch2:		libiec61883-02-struct.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
cp %SOURCE1 src/byteswap.h
cp %SOURCE2 src/endian.h
cp %SOURCE2 examples/endian.h

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

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Sep  4 2007 - dougs@truemail.co.th
- Initial base spec file
