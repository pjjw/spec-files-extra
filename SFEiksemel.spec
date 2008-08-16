#
# Copyright (c) 2006 Halo Kwadrat Sp. z o. o. (http://www.halokwadrat.pl)
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
Summary: XML-parsing library
Name: SFEiksemel
Version: 1.3
Release: 1
License: LGPL
Group: Development/Libraries
URL: http://code.google.com/p/iksemel/
SUNW_BaseDir:	%{_prefix}
BuildRoot:  %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Source: http://iksemel.googlecode.com/files/iksemel-%{version}.tar.gz
# BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: SUNWgnutls-devel

%description
This is an XML parser library mainly designed for Jabber applications.
It provides SAX, DOM, and special Jabber stream APIs. Library is coded
in ANSI C except the network code (which is POSIX compatible), thus
highly portable.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
%include default-depend.inc


%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.


%prep 
mkdir -p %{name}-%{version}
%setup -q -n iksemel-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="%{_ldflags} -L/usr/gnu/lib -R/usr/gnu/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --infodir=%{_infodir} \
	    --datadir=%{_datadir}
make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_infodir}
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO
%doc %{_infodir}/iksemel*
%{_infodir}/iksemel
%{_bindir}/ikslint
%{_bindir}/iksperf
%{_bindir}/iksroster
%{_libdir}/libiksemel.so.*

%files devel
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_includedir}/iksemel.h
%{_libdir}/libiksemel.so
%{_libdir}/pkgconfig/iksemel.pc
%{_libdir}/libiksemel.la
%{_libdir}/libiksemel.a

%changelog
* Fri Aug 15 2008 Michal Bielicki - 1.3-2
- OpenSolarised for SFE

* Fri Jul 03 2007 Dries Verachtert  - 1.3-1
- Updated to release 1.3.

* Sat Apr 08 2006 Dries Verachtert  - 1.2-1.2
- Rebuild for Fedora Core 5.

* Thu Dec 08 2005 Dries Verachtert  - 1.2-1
- Initial package.

