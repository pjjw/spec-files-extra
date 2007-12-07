#
# spec file for package SFEwmfire
#
# includes module(s): wmfire
#
%include Solaris.inc

Name:                    SFEwmfire
Summary:                 Wmfire Docapp
Version:                 1.2.3
Source:                  http://dockapps.org/download.php/id/649/wmfire-%{version}.tar.gz
URL:                     http://www.swanson.ukfsn.org/
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n wmfire-%version

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

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
- Initial wmfire spec file

