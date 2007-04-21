#
# spec file for package libopensync
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

Name:           aria2
License:        GPL
Group:          Applications/Internet
Version:        0.9.0
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://aria2.sourceforge.net/
Summary:        Download utility with BitTorrent and Metalink support
Source:         http://umn.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.bz2
Patch1:         %{name}-01-wall.diff
Patch2:         %{name}-02-main.diff
Patch3:         %{name}-03-include-order.diff
Patch4:         %{name}-04-array-size.diff
Patch5:         %{name}-05-ctime.diff
Patch6:         %{name}-06-countif.diff
Patch7:         %{name}-07-init-str.diff
Patch8:         %{name}-08-libgen.diff

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/doc

BuildRequires: openssl-devel, libxml2-devel, gcc-c++, gettext

%description
aria2 is a download utility with resuming and segmented downloading.
Supported protocols are HTTP/HTTPS/FTP/BitTorrent/Metalink.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
 
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

libtoolize --force
# aclocal $ACLOCAL_FLAGS -I .
autoheader
automake-1.9 -a -c -f
autoconf
./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
            --mandir=%{_mandir}                 \
            --disable-static                    \

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root)
%doc ChangeLog COPYING NEWS README AUTHORS TODO
%{_bindir}/aria2c
%{_mandir}/man1/aria2c*

%changelog
* Sat Apr 21 2007 - dougs@truemail.co.th
- Forced build to used automake-1.9
* Tue Dec 19 2006 - halton.huo@sun.com
- Initial version
