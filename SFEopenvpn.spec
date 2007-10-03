#
# spec file for package SFEopenvpn
#
# includes module(s): openvpn
#
%include Solaris.inc

Name:		SFEopenvpn
Summary:	Opensource, full-featured SSL VPN package
Version:	2.0.9
Source:		http://openvpn.net/release/openvpn-%{version}.tar.gz
Source1:	http://www.whiteboard.ne.jp/~admin2/tuntap/source/openvpn/tun.c
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElzo
Requires: SFElzo
BuildRequires: SFEtun
Requires: SFEtun

%prep
%setup -q -n openvpn-%version
cp %SOURCE1 .

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -R/usr/sfw/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --with-ssl-headers=/usr/sfw/include \
            --with-ssl-lib=/usr/sfw/lib

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/openvpn
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/openvpn.8

%changelog
* Wed Oct  3 2007 - Doug Scott <dougs@truemail.co.th>
- Added modified tun.c
* Wed Apr 07 2007 - Eric Boutilier
- Initial spec
