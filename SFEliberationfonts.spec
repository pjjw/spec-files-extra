#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEliberationfonts
License:             GPL+exception
Summary:             OpenSource TrueType fonts from RedHat
Version:             0.2
URL:                 https://www.redhat.com/promo/fonts/
Source:              http://www.redhat.com/f/fonts/liberation-fonts-ttf-3.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWTk

%prep
%setup -q -n liberation-fonts-%version

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/openwin/lib/X11/fonts/TrueType
cp * ${RPM_BUILD_ROOT}%{_prefix}/openwin/lib/X11/fonts/TrueType

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/fc-cache

%postun
/usr/bin/fc-cache

%files
%defattr (-, root, bin)
%{_prefix}/*

%changelog
* Sun Feb 03 2008 - moinak.ghosh@sun.com
- Initial spec.
