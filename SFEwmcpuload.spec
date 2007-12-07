#
# spec file for package SFEwmfire
#
# includes module(s): wmcpuload
#
%include Solaris.inc

Name:                    SFEwmcpuload
Summary:                 Wmcpuload Dockapp
Version:                 1.0.1
Source:                  http://dockapps.org/download.php/id/59/wmcpuload-%{version}.tar.bz2
URL:                     http://www.sh.rim.or.jp/~ssato/dockapp/index.shtml#wmcpuload
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n wmcpuload-%version

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \

gmake

%install
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1/*

%changelog
* Sat Aug 11 2007 - pradhap (at) gmail.com
- Initial wmcpuload spec file

