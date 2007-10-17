#
# spec file for package sane-backends.spec
#
#
Name:         sane-backends
License:      GPL
Group:        Hardware/Other
Version:      1.0.18
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      SANE - Scanner Access Now Easy - backends
Source:	      http://alioth.debian.org/frs/download.php/1669/sane-backends-%{version}.tar.gz
# date:2007-02-25 bugzilla: owner:xz159989 type:feature
Patch1:       sane-backends-01-disable-saned.diff
URL:          http://www.sane-project.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
DocDir:       %{_defaultdocdir}/sane

%package devel
Summary:      %{summary} - development files
Group:        Development/Libraries
Requires:     %name 

%prep
%setup -q
%patch1 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif

./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
	    --mandir=%{_mandir}                 \
            --docdir=%{_datadir}/doc            \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info
	    		
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/lib*.so*
%{_libdir}/sane
%{_datadir}/sane
%{_datadir}/doc/*
%{_mandir}/*/*
%config %{_sysconfdir}/*


%files devel
%defattr (-, root, root)
%{_includedir}/*

%changelog
* Tue Mar 20 2007 - simon.zheng@sun.com
- initial version for pkgbuild
- Add patch sane-backends-01-disable-saned.diff
