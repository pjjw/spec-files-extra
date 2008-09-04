#
# spec file for package openobex
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
# bugdb: http://dev.zuckschwerdt.org/openobex/ticket/
#

Name:           openobex
License:        LGPL
Group:          System/Libraries
Version:        1.3
Release:        1
URL:            http://dev.zuckschwerdt.org/openobex
Summary:        OpenOBEX - open source implementation of the Object Exchange protocol
Source:         http://%{sf_mirror}/sourceforge/openobex/openobex-%{version}.tar.gz
Patch1:         openobex-01-sun-studio.diff
Patch2:         openobex-02-libusb.diff
Patch3:         openobex-03-PACKED.diff
Patch4:         openobex-04-func.diff
Patch5:         openobex-05-zero-array.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/doc

%package devel
Summary:		Header files, libraries and development documentation for %{name}
Group:			Development/Libraries
Requires:		%{name} = %{version}

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
	    --mandir=%{_mandir}			\
            --enable-usb                        \
%if %debug_build
	    --enable-debug                      \
%endif
	    --disable-static

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri. Oct. 26 - jijun.yu@sun.com
- Add the patch openobex-05-zero-array.diff
* Fri. Oct. 19 - jijun.yu@sun.com
- Enable debug option and add the patch openobex-04-func.diff
* Thu July 07 2007 - jijun.yu@sun.com
- Modify the URL
* Thu July 07 2007 - jijun.yu@sun.com
- Add a patch
* Mon Apr  2 2007 - laca@sun.com
- Initial version
