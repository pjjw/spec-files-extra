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
Version:                0.27
Source:                 %{sf_download}/freeassociation/libical-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWPython
BuildRequires: SUNWPython-devel
Requires: SUNWperl584core
BuildRequires: SUNWperl584usr
BuildRequires: SFEswig

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n libical-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


SFWLIBS="-L/usr/sfw/lib -R/usr/sfw/lib"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags $SFWLIBS"
./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes		\
	    --enable-static=no		\
            --enable-python

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,other) %{_datadir}/libical
%{_datadir}/libical/*

%files devel
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Jan  21 2008 - moinak.ghosh@sun.com
- Initial spec.
