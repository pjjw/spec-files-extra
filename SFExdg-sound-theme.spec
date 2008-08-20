 
# spec file for package SFExdg-sound-theme
#
# includes module(s): xdg-sound-theme
#
%include Solaris.inc

Name:                    SFExdg-sound-theme
Summary:                 XDG FreeDesktop Sound Theme
Version:                 0.1
URL:                     http://0pointer.de/blog/projects/sixfold-announcement.html
Source:                  http://0pointer.de/public/sound-theme-freedesktop.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
mkdir -p xdg-sound-theme
cd xdg-sound-theme
gunzip -c sound-theme-freedesktop.tar.gz | tar xf -

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/sounds
tar cpf - freedesktop | (cd ${RPM_BUILD_ROOT}/%{_datadir}/sounds; tar xpf - )

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/sounds
%{_datadir}/sounds/*

%changelog
* Thu Aug 20 2008 - brian.cameron@sun.com
- Created.
