#
# spec file for package at-poke
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
Name:         at-poke
License:      LGPL
Group:        System/Libraries/GNOME
Version:      0.2.3
Release:      40
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Tool to poke around accessibility infrastructure
Source:       http://ftp.gnome.org/pub/GNOME/sources/at-poke/0.2/%{name}-%{version}.tar.bz2
URL:          http://developer.gnome.org/projects/gap
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define libgnomeui_version 2.4.0.1
%define gtk2_version 2.2.4
%define atk_version 1.4.0
%define at_spi_version 1.1.8
%define libgail_gnome_version 1.0.2

# Requirements: libgail-gnome libglade-2.0
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: at-spi-devel >= %{at_spi_version}
BuildRequires: libgail-gnome >= %{libgail_gnome_version}
Requires:      atk >= %{atk_version}
Requires:      gtk2 >= %{gtk2_version}
Requires:      libgnomeui >= %{libgnomeui_version}
Requires:      at-spi >= %{at_spi_version}
Requires:      libgail-gnome >= %{libgail_gnome_version}

%description
at-poke is a tool that allows one to examine the widigts from an accessibility perspective.

%prep
%setup -q 

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

./configure --prefix=%{_prefix}

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/at-poke
%{_datadir}/at-poke/at-poke.glade2
%{_mandir}/man1/*


%changelog
* Mon Aug 21 2006 - brian.cameron@sun.com
- Fix location of gtk-demo so at-poke can launch it.
* Tue Apr 18 2006 - padraig.obriain@sun.com
- Add patch at-poke-01-crash.diff for bug 6413890
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 0.2.3.
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add at-poke.1 manpage
* Wed Aug 18 2004 - brian.cameron@sun.com
- removed --disable-gtk-doc since this isn't an option this module's
  configure takes.
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed Feb 25 2004 - damien.carbery@sun.com
- Initial release version for at-poke
