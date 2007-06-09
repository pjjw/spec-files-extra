#
# spec file for package SFEhpoj
#
# includes module(s): hpoj
#
%include Solaris.inc

%define src_name	hpoj
%define src_url		http://heanet.dl.sourceforge.net/sourceforge/%{src_name}

Name:                   SFEhpoj
Summary:                HPOJ - HP OfficeJet driver
Version:                0.91
Source:                 %{src_url}/%{src_name}-%{version}.tgz
Patch1:                 hpoj-01-build.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
Requires: %name
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CC=gcc
export CXX=g++
export CFLAGS="%{gcc_optflags}"
export CXXFLAGS="%{gcc_cxx_optflags}"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --with-libusb=/usr/sfw      \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		

make SHELL=/bin/bash -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make SHELL=/bin/bash install \
    prefix=$RPM_BUILD_ROOT/%{_prefix} \
    bindir=$RPM_BUILD_ROOT/%{_bindir} \
    sbindir=$RPM_BUILD_ROOT/%{_sbindir} \
    libdir=$RPM_BUILD_ROOT/%{_libdir} \
    includedir=$RPM_BUILD_ROOT/%{_includedir} \
    docdir=$RPM_BUILD_ROOT/%{_datadir}/doc/hpoj
cd $RPM_BUILD_ROOT/%{_libdir}
mkdir sane
mv libsane-hpoj.so* sane/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/sane
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/hpoj

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Jun  8 2007 - laca@sun.com
- Initial version
