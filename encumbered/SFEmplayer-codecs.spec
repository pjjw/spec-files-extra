#
# spec file for package SFEmplayer-codecs.spec
#
# includes module(s): "essential" codecs from the mplayer project
#
# BIG FAT WARNING: This package contains Win32 codec DLLs, it may or may
#                  not be legal to use these even if you have purchased
#                  a license for Windows
#

%include Solaris.inc

Name:                    SFEmplayer-codecs
Summary:                 binary codecs for the mplayer movie player
%define year  2007
%define month 10
%define day   07
Version:                 %{year}.%{month}.%{day}
Source:                  http://www1.mplayerhq.hu/MPlayer/releases/codecs/essential-%{year}%{month}%{day}.tar.bz2
URL:                     http://www.mplayerhq.hu/design7/dload.html
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n essential-%{year}%{month}%{day}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/mplayer/codecs
cp * $RPM_BUILD_ROOT%{_libdir}/mplayer/codecs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin) 
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/mplayer/codecs

%changelog
* Tue Sep 02 2008 - nonsea@users.sourceforge.net
- No use undefined %{mplayer.codecdir}
* Sun Nov 04 2007 - markwright@internode.on.net
- Bump to 20071007
* Sun Jan  7 2007 - laca@sun.com
- separate from the rest of mplayer
