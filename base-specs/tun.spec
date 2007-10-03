#
#
# spec file for package tun
#
# includes module(s): tun
#

%define src_name tuntap
%define src_url http://www.whiteboard.ne.jp/~admin2/tuntap/source/%{src_name}

Name:                tun
Summary:             Virtual Point-to-Point network device
Version:             1.1.1
Source:              %{src_url}/%{src_name}.tar.gz
Patch1:		     tun-01-solaris.diff
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}
%patch1 -p1

%build
./configure --prefix=%{_prefix}
make

%install
install -D if_tun.h $RPM_BUILD_ROOT%{_includedir}/net/if_tun.h
install -D tun $RPM_BUILD_ROOT${drv_dir}
install -D tap $RPM_BUILD_ROOT${drv_dir}
%ifarch sparcv9 amd64
install -D tun64 $RPM_BUILD_ROOT${drv_dir}/%{_arch64}
install -D tap64 $RPM_BUILD_ROOT${drv_dir}/%{_arch64}
%endif
install -D tun.conf $RPM_BUILD_ROOT${drv_base}/tun.conf

%changelog
* Wed Oct  3 2007 - Doug Scott
- Updated to build tap from latest source
* Wed Apr 07 2007 - Eric Boutilier
- Initial spec
