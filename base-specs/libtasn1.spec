#
# License (c) 2008 Sun Microsystems Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jefftsai
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=245&atid=100245&aid=
#
Name:     	libtasn1
Version: 	1.4
Release:        0
Vendor:		Sun Microsystems, Inc.
Distribution:	Java Desktop System
License:	LGPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:         %{_datadir}/doc
Autoreqprov:	on
URL:		http://www.sun.com/software/javadesktopsystem/
Epoch:		2
Source:		ftp://ftp.gnutls.org/pub/gnutls/libtasn1/%{name}-%{version}.tar.gz
Summary:	Libtasn is a library written in C for manipulating ASN.1 objects.

%description
Libtasn is a library written in C for manipulating ASN.1 objects including 
DER/BER encoding and DER/BER decoding. Libtasn is used by GnuTLS to manipulate 
X.509 objects and by GNU Shishi to handle Kerberos V5 packets.

%package -n libtasn1-devel
Summary:	Static libraries and header files for libtasn1
Group:		Applications/Text
Requires:	libtasn1 => %{version}-%{release}

%description -n libtasn1-devel
The libtasn1-devel package includes the static libraries and header 
files needed for tasn1 development.

%files -n libtasn1-devel
%defattr(-, root, root)
%{_libdir}/*.so*
%{_includedir}/*

%prep
%setup  -q -n %{name}-%{version}

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

aclocal $ACLOCAL_FLAGS -I m4 -I gl/m4
libtoolize --force --copy
autoconf
automake -a -c -f

./configure --prefix=%{_prefix}                        \
            --bindir=%{_bindir}                        \
            --libdir=%{_libdir}                        \
            --sysconfdir=%{_sysconfdir}                \
            --includedir=%{_includedir}        \
            --mandir=%{_mandir}                        \
           --infodir=%{_infodir}               \
           --disable-rpath                     \
           --disable-static                    \
           --enable-shared



make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT mkdir_p="mkdir -p"
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT%{_datadir}/info
rm -rf $RPM_BUILD_ROOT/usr/local
rm -rf $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Mar 28 2007 - jeff.cai@sun.com
- Split to two spec files.
