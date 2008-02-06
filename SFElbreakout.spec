#
# spec file for package SFElbreakout
#
#
%include Solaris.inc

Name:                    SFElbreakout
Summary:                 LBreakout is a breakout-style arcade game in the manner of Arkanoid.
Version:                 010315
Source:                  http://prdownloads.sourceforge.net/lgames/lbreakout-%{version}.tar.gz
URL:                     http://lgames.sourceforge.net/index.php?project=LBreakout
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n lbreakout-%version

%build
mkdir -p $RPM_BUILD_ROOT/var/lib/games
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} 
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
%{_datadir}/*


%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, other) /var/lib
%dir %attr (0755, root, other) /var/lib/games
/var/lib/games/*


#%dir %attr(0755, root, bin) %{_mandir}
#%dir %attr(0755, root, bin) %{_mandir}/man1/*

%changelog
- Wed Feb  6 pradhap (at) gmail.com
- Initial lbreakout spec file.

