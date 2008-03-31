#
# spec file for package SFEfortune
#
# includes module(s): fortune
#
%include Solaris.inc

Name:                    SFEfortune
Summary:                 Fortunes contained in the fortune database.
Version:                 1.99.1
Source:                  http://ftp.de.debian.org/debian/pool/main/f/fortune-mod/fortune-mod_%{version}.orig.tar.gz
URL:                     http://ftp.de.debian.org/debian/pool/main/f/fortune-mod/
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
patch0:                  fortune.01.diff
patch1:                  fortune.02.diff

%include default-depend.inc

Requires: SUNWcsu
Requires: SFErecode

%prep
%setup -q -n fortune-mod-%version
%patch0 -p1
%patch1 -p1

%build
gmake

%install
gmake install prefix=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT/usr/bin
ln -s ../games/fortune ./fortune 
cd -

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, sys) /usr/share

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, bin) /usr/games
/usr/games/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man6/*

%dir %attr (0755, root, sys) %{_datadir}/games
%{_datadir}/games/*


%changelog
* Mar 31 2008 - pradhap (at) gmail.com
- Initial fortune spec file.

