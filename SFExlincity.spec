#
# spec file for package SFExlincity
#

%include Solaris.inc
Name:                    SFExlincity
Summary:                 xlincity - Simulation game based on opensourced components of S*mc*ty. 
Group:                   Game/Simulation
URL:                     http://lincity.sourceforge.net 
Version:                 1.12.0
Source:                  http://www.ibiblio.org/pub/Linux/games/strategy/lincity-1.12.0.tar.gz 
Patch1:			 xlincity-01-solaris.diff
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%prep
%setup -q  -n lincity-%{version} 
find ./intl -name \*.c -exec dos2unix {} {} \;
find ./intl -name \*.h -exec dos2unix {} {} \;
find ./intl -name \*.charset -exec dos2unix {} {} \;
%patch1 -p1

%build
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
/usr/local/share/lincity/*
/usr/local/lib/charset.alias
/usr/local/share/locale/ca/LC_MESSAGES/lincity.mo
/usr/local/share/locale/it/LC_MESSAGES/lincity.mo
/usr/local/share/locale/locale.alias
/usr/local/bin/xlincity
/usr/local/man/man6/lincity.6


%changelog
* Wed Jan 23 2008 - Brian Nitz - <brian dot nitz at sun dot com> 
- Initial version.
