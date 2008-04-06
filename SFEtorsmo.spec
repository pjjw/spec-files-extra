#
# spec file for package SFEtorsmo
#
# includes module(s): torsmo
#
%include Solaris.inc

Name:                    SFEtorsmo
Summary:                 Tyopoyta ORvelo System MOnitor
Version:                 0.17
Source:                  http://downloads.sourceforge.net/belenixtools/torsmo-%{version}.tar.gz
URL:                     http://torsmo.sourceforge.net/
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#patch0:                  fortune.01.diff

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n torsmo-%version
#%patch0 -p1

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
mkdir $RPM_BUILD_ROOT/etc
cp torsmorc.sample $RPM_BUILD_ROOT/etc/torsmorc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, sys) /usr/share

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%attr(0644, root, sys) %{_sysconfdir}/torsmorc

%changelog
* Apr Sun 6 2008 - pradhap (at) gmail.com
- Initial fortune spec file.
- Thanks to Alexander R. Eremin eremin@rosbi.ru for Solaris port
