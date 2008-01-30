#
# spec file for package SFEdcraw
#

%include Solaris.inc
Name:                    SFEdcraw
Summary:                 dcraw - Decoding RAW digital photos in Linux
URL:                     http://www.cybercom.net/~dcoffin/dcraw/
#Version:                 1.0.0
Version:                 8.80
#Source:                  http://www.cybercom.net/~dcoffin/dcraw/dcraw.c
Source:                  http://ftp.de.debian.org/debian/pool/main/d/dcraw/dcraw_%{version}.orig.tar.gz
Patch1:			 dcraw-01-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires: SFElcms
%include default-depend.inc


%prep
#%setup -c -T -n dcraw-%version
#cp %SOURCE0 .
%setup -q -n dcraw-%{version}.orig
%patch1 -p1

%build
cc -o dcraw dcraw.c -lm -ljpeg -llcms

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp dcraw $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*


%changelog
* Fri Nov 16 2007 - Damien Carbery <daymobrew@users.sourceforge.net>
- Initial version.
