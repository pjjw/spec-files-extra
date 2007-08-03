#
# spec file for package SFElibmspack
#
# includes module(s): libmspack
#
%include Solaris.inc

%define	src_ver 0.0.20060920alpha
%define	src_name libmspack
%define	src_url	http://www.kyz.uklinux.net/downloads

Name:		SFElibmspack
Summary:	A library for Microsoft compression formats
Version:	%{src_ver}
License:	GPL v2
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libmspack-01-wall.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
The purpose of libmspack is to provide compressors and decompressors,
archivers and dearchivers for Microsoft compression formats: CAB, CHM,
HLP, KWAJ, LIT and SZDD. It is also designed to be easily embeddable,
stable, robust and resource-efficient.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-D__FUNCTION__=__func__"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal
autoconf -f
autoheader
automake -a -f
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared			\
	    --disable-debug

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
