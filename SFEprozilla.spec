#
# Author pradhap
# spec file for package SFEprozilla
#
# includes module(s): Prozilla
#
%include Solaris.inc

Name:                    SFEprozilla
Summary:                 Prozilla download accelerator
Version:                 2.0.4
Source:                  http://prozilla.genesys.ro/downloads/prozilla/tarballs/prozilla-%{version}.tar.bz2
URL:                     http://prozilla.genesys.ro/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Patch1:                  prozilla-solaris.patch

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n prozilla-%version
%patch1 -p1

%build
./configure --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --infodir=%{_infodir} \
	--disable-nls \
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

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/prozilla
%{_includedir}/prozilla/*

%changelog
* Wed Aug 20 2008 - pradhap (at) gmail.com
- Initial prozilla spec file.

