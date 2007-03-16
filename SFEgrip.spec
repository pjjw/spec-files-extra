#
# spec file for package SFEgst-python
#
# includes module(s): gst-python
#

%include Solaris.inc
Name:                    SFEgrip
Summary:                 Cd-player and cd-ripper for the Gnome desktop
URL:                     http://nostatic.org/grip/
Version:                 3.3.1
Source:                  http://prdownloads.sourceforge.net/grip/grip-%{version}.tar.gz
Patch1:			 grip-01-i386.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -q -n grip-%version
%patch1 -p1

%build
export LDFLAGS="-lX11"
./configure --prefix=%{_prefix} --disable-shared-cdpar --disable-shared-id3
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#move locale to /usr/share
mv $RPM_BUILD_ROOT%{_libdir}/locale $RPM_BUILD_ROOT%{_datadir}/
rm -rf $RPM_BUILD_ROOT%{_libdir}
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%{_bindir}/grip
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnome/help/grip
%{_datadir}/applications/grip.desktop
%{_datadir}/pixmaps/gripicon.png
%{_datadir}/pixmaps/griptray.png
%{_datadir}/locale/*/LC_MESSAGES/grip-2.2.mo

%changelog
* Fri Mar 16 2007  - irene.huang@sun.com
- created
