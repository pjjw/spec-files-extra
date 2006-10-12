#
# spec file for package SFEconnect
#
# includes module(s): connect
#

%include Solaris.inc
Name:                    SFEconnect
Summary:                 Proxy command of OpenSSH
Version:                 1.95
Source1:                 http://www.taiyo.co.jp/~gotoh/ssh/connect.c
SUNW_BaseDir:            %{_basedir}
URL:                     http://zippo.taiyo.co.jp/~gotoh/ssh/connect.html
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
test -d %name-%version && rm -rf %name-%version
mkdir %name-%version
install %SOURCE1 %name-%version

%build
cd %name-%version
cc connect.c -o connect -lnsl -lsocket -lresolv

%install
cd %name-%version
rm -rf $RPM_BUILD_ROOT
install -d --mode=0755 $RPM_BUILD_ROOT%{_bindir}
install --mode=0555 connect $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Wed Oct 11 2006 - laca@sun.com
- fix prep so it that %name-%version dir is always created
* Tue Sep 26 2006 - halton.huo@sun.com
- Initial spec file
