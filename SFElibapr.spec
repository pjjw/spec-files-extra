#
# spec file for package SFElibapr
#
#
%include Solaris.inc
%include usr-gnu.inc

Name:			SFElibapr
License:		Apache,LGPL,BSD
Group:			system/dscm
Version:		1.2.12
Summary:		Apache Portable Runtime
Source:			http://apache.ziply.com/apr/apr-%{version}.tar.gz
URL:			http://apr.apache.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWcsl
Requires: SUNWcsr
Requires: SFEgawk

%description
Apache Portable Runtime (APR) provides software libraries
that provide a predictable and consistent interface to
underlying platform-specific implementations.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:                SUNWhea

%prep
%setup -q -n apr-%{version}

%build
export PATH=/usr/ccs/bin:/usr/gnu/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin:/opt/jdsbld/bin
export CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --disable-static \
    --with-pic \
    --with-installbuilddir=%{_datadir}/apr/build \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-threads
    
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/apr/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Initial spec.
