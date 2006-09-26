#
# spec file for package SFEdante
#
# includes module(s): dante
#


%include Solaris.inc
Name:                    SFEdante
Summary:                 Tool connecting to external networks via SOCKS.
Version:                 1.1.19
License:                 BSD/Carnegie Mellon University
Source:                  ftp://ftp.inet.no/pub/socks/dante-%{version}.tar.gz
Source1:                 ftp://ftp.inet.no/pub/socks/extracted/example/socks.conf
SUNW_BaseDir:            %{_basedir}
URL:                     http://www.inet.no/dante/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%description
Dante is a circuit-level firewall/proxy that can be used to provide convenient
and secure network connectivity to a wide range of hosts while requiring only
the server Dante runs on to have external network connectivity.

%prep
%setup -q -n dante-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

aclocal $ACLOCAL_FLAGS
libtoolize --force
glib-gettextize --force --copy
intltoolize --force --automake
autoheader
automake -a -f -c --gnu
autoconf
./configure --prefix=%{_prefix} \
	    --bindir=%{_bindir} \
	    --libdir=%{_libdir} \
	    --datadir=%{_datadir} \
	    --sysconfdir=%{_sysconfdir} \
	    --mandir=%{_mandir} \
	    --sbindir=/usr/sbin
	    
make -j $CPU

%install
rm -rf $RPM_BUILD_ROOT
make -i install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
install -d --mode=0755 $RPM_BUILD_ROOT%{_sysconfdir}
install --mode=0644 %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) /usr/sbin
/usr/sbin/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/man*/* 

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Sep 26 2006 - halton.huo@sun.com
- Initial spec file
