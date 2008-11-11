#
# spec file for package SFEopenexr.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                   SFElibical
Summary:                Libical is an Open Source implementation of the IETF's iCalendar Calendaring and Scheduling protocols
Version:                0.41
Source:                 %{sf_download}/freeassociation/libical-%{version}.tar.gz
# owner:jedywang date:2008-10-30 type:branding
Patch1:              libical-01-build.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWperl584core
BuildRequires: SUNWperl584usr
BuildRequires: SFEcmake

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n libical-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


mkdir build && cd build
%if %debug_build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Debug \
		-DICAL_ERRORS_ARE_FATAL=false ..
%else
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DICAL_ERRORS_ARE_FATAL=false \
		..
%endif
make

%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue Nov  11 2008 - jedy.wang@sun.com
- Bump to 0.4.1.
* Thu Oct  30 2008 - jedy.wang@sun.com
- Bump to 0.4.0.
- Use cmake to build.
- Add patch 01-build.diff.
* Mon Jan  21 2008 - moinak.ghosh@sun.com
- Initial spec.
