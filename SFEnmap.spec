#
# spec file for package SFEnmap
#
# includes module(s): nmap
#
%include Solaris.inc

Name:         SFEnmap
Summary:      Network Mapper
License:      GPL
Version:      4.20
Group:        System/GUI/GNOME
Source:       http://download.insecure.org/nmap/dist/nmap-%{version}.tar.bz2
Patch1:       nmap-01-__FUNCTION__.diff
Patch2:       nmap-02-Makefile.diff
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
URL:          http://insecure.org/nmap/index.html

%include default-depend.inc

%description
Nmap ("Network Mapper") is a free open source utility for network exploration or security auditing.

%prep
%setup -q -n nmap-%version
%patch1 -p1
%patch2 -p1


%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

%if %cc_is_gcc
export NMAP_CXX="$CXX"
%else
export NMAP_CXX="${CXX} -norunpath"
%endif

export CXXFLAGS="%opt_cxxflags -features=extensions"

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir}

make -j $CPUS CXX="$NMAP_CXX"

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/nmap
%{_datadir}/nmap/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%changelog
* Thu Jan 11 2007 - dermot.mccluskey@sun.com
- Initial version
