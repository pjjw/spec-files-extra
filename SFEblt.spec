#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc


Name:                SFEblt
Summary:             BLT - Bluetooth Location Tracker
Version:             0.15
Source:              http://www.betaversion.net/blt/blt_server-%{version}.tgz
Patch1:              blt-01-solaris.diff
URL:                 http://www.betaversion.net/blt/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%prep
%setup -q -n blt_server-%{version}
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp blt_server            $RPM_BUILD_ROOT%{_bindir}
cp blt_device_names.dn   $RPM_BUILD_ROOT%{_bindir}
cp blt_location_names.ln $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Wed Nov 21 2007 - daymobrew@users.sourceforge.net
- Initial spec
