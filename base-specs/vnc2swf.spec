# spec file for package vnc2swf 
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#

Name:        vnc2swf
Version:     0.5.0
Release:     1
Summary:     Vnc2Swf is a recoding tool for Flash.
Copyright:   GPL
URL:         http://www.unixuser.org/~euske/vnc2swf/
Source:      http://www.unixuser.org/~euske/vnc2swf/vnc2swf-%{version}.tar.gz
BuildRoot:   %{_tmppath}/%{name}-%{version}-root
Requires:    zlib XFree86-libs libstdc++

%description
Vnc2Swf is a screen recoding tool for Flash.

%prep
%setup -q

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

./configure --prefix=%{_prefix}

make -j $CPUS

%install
rm -rf ${RPM_BUILD_ROOT}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-, root, root)
/usr/X11R6/bin/vnc2swf
%doc README
%doc README.vnc-3.3.7

%changelog
* Mon Jul 30 2007 - nonsea@users.sourceforge.net
- Initial spec
