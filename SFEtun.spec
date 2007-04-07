#
#
# spec file for package SFEtun
#
# includes module(s): tun
#
%include Solaris.inc

Name:                SFEtun
Summary:             Virtual Point-to-Point network device
Version:             1.1
Source:              http://vtun.sourceforge.net/tun/tun-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n tun-%version

%build
export CC=/usr/sfw/bin/gcc
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"

cd solaris
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
cd solaris 
install -D if_tun.h $RPM_BUILD_ROOT%{_includedir}/net/if_tun.h
install -D tun $RPM_BUILD_ROOT/usr/kernel/drv/tun
install -D tun.conf $RPM_BUILD_ROOT/usr/kernel/drv/tun.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'retval=0';
  echo 'add_drv tun || retval=1';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'rem_drv tun || retval=1';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/net
%{_includedir}/net/if_tun.h
%dir %attr (0755, root, sys) /usr/kernel
%dir %attr (0755, root, sys) /usr/kernel/drv
/usr/kernel/drv/tun
/usr/kernel/drv/tun.conf

%changelog
* Wed Apr 07 2007 - Eric Boutilier
- Initial spec
