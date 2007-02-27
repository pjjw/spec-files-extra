#
# spec file for package SFEethereal
#
# includes module(s): ethereal
#
%include Solaris.inc

Name:         SFEethereal
Summary:      Ethereal network protocol analyzer
Version:      0.99.0
Source:       http://www.ethereal.com/distribution/ethereal-0.99.0.tar.bz2
Patch0:       ethereal-01-emem.diff
URL:          http://www.ethereal.com
License:      GPL
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWopenssl-libraries
Requires: SFElibpcap
BuildRequires: SUNWperl584core
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWopenssl-include
BuildRequires: SFElibpcap-devel

%prep
%setup -q -n ethereal-%version
%patch0 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export PATH="/usr/xpg4/bin:/usr/perl5/bin:$PATH"
export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}	     \
            --disable-usr-local              \
            --enable-threads                 \
            --with-ssl=/usr/sfw              \
            --without-net-snmp

make -j $CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
	
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/man1/*
%{_mandir}/man4/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/ethereal
%{_datadir}/ethereal/*

%changelog
* Tue Feb 27 2007 - laca@sun.com
- set CFLAGS and LDFLAGS for optimizations
* Mon Feb 26 2007 - ivwang@gmail.com
- Initial version
