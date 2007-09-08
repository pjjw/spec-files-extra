#
# spec file for package SFEazureus
#
# includes module(s): azureus
#
%include Solaris.inc
%define _desktopdir %{_datadir}/applications
%define _pixmapsdir %{_datadir}/pixmaps

%define src_name Azureus
%define src_ver 3.0.2.2
%define src_url http://dl.sourceforge.net/azureus

Name:		SFEazureus
Summary:	Azureus - Java BitTorrent client
Version:	%{src_ver}
License:	GPL
Group:		X11/Applications/Networking
Source:		%{src_url}/%{src_name}_%{src_ver}_source.zip
Source1:	azureus.png
Source2:	azureus.desktop
Source3:	azureus.sh
Patch1:		azureus-01-buildfile.diff
Patch2:		azureus-02-unixonly.diff
URL:		http://azureus.sourceforge.net/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEeclipse
Requires: SFEjakarta-commons-cli
Requires: SFElogging-log4j
Requires: SFEjunit

%prep
%setup -q -c -n %{name}-%{version}
find . -name \*.java -exec dos2unix {} {} \;
find . -name \*.xml  -exec dos2unix {} {} \;
%patch1 -p1
%patch2 -p1
install -d build/libs

%build
rm -rf org/gudy/azureus2/platform/{win32,macosx}
rm -rf org/gudy/azureus2/ui/swt/{win32,osx,test}
rm -rf com/aelitis/azureus/util/win32
export ANT_OPTS="-Xms256m -Xmx256m"
ant

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_datadir}/Azureus,%{_pixmapsdir},%{_desktopdir},%{_bindir}}

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/azureus
install dist/Azureus.jar $RPM_BUILD_ROOT%{_datadir}/Azureus/Azureus.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%attr(755,root,bin) %{_bindir}
%dir %attr(755,root,sys) %{_datadir}
%dir %attr(755,root,other) %{_desktopdir}
%{_desktopdir}/azureus.desktop
%dir %attr(755,root,other) %{_pixmapsdir}
%{_pixmapsdir}/azureus.png
%{_datadir}/Azureus

%changelog
* Sat Sep  8 2007 - dougs@truemail.co.th
- Initial version
