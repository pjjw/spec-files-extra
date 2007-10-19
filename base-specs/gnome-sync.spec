#
# spec file for package gnome-sync
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Summary:	Gnome Synchronization GUI tool
Name:		gnome-sync
License:    GPL
Version:	0.2.0
Release:	1
Group:		System/GUI/GNOME
URL:		http://gnome-sync.org/
Vendor:		Sun Microsystems, Inc.
Source:		http://superb-east.dl.sourceforge.net/sourceforge/gnome-sync-tool/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:		%{_defaultdocdir}/doc

%define     glib2_version 2.8.0
%define     gtk2_version 2.8.0
%define     GConf_version 2.12.0
%define     libglade_version 2.3.0
%define     opensync_version 0.32
%define     libedataserverui_version 1.10.1
%define     libxml_version 2.0.0

Requires: 	glib2 >= %{glib2_version}
Requires: 	gtk2 >= %{gtk2_version}
Requires: 	GConf >= %{GConf_version}
Requires: 	libglade >= %{libglade_version}
Requires: 	libopensync >= %{opensync_version}
Requires: 	libedataserverui >= %{libedataserverui}
Requires: 	libxml >= %{libxml_version}

BuildRequires:      glib2-devel    >= %{glib2_version}
BuildRequires:      gtk2-devel     >= %{gtk2_version}
BuildRequires:      GConf-devel    >= %{GConf_version}
BuildRequires:      libglade-devel >= %{libglade_version}
BuildRequires: 	    libopensync-devel >= %{opensync_version}
BuildRequires:      libedataserverui-devel >= %{libedataserverui}
BuildRequires:      libxml-devel >= %{libxml_version}

Distribution: 	Any
Packager:     	Halton Huo <halton.huo@sun.com>

%description
gnome-sync is a Gnome Synchronization GUI tool, it use libopensync as sync engine, 
for more information, please visit http://www.opensync.org

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

aclocal $ACLOCAL_FLAGS
libtoolize --force
intltoolize --force --automake
autoheader
automake -a -f -c --gnu
autoconf

CFLAGS="$RPM_OPT_FLAGS"                 \
./configure   --prefix=%{_prefix}           \
          --sysconfdir=%{_sysconfdir}       \
          --libexecdir=%{_libexecdir}       \

make  -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gnome-sync.schemas >/dev/null

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL MAINTAINERS NEWS README TODO

%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/gnome/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/%{name}
%{_datadir}/locale
%config %{_sysconfdir}/gconf/schemas/*

%changelog
* Fri Oct 19 2007 - halton.huo@sun.com
- Change Source URL to a usable one.
* Thu Oct 18 2007 - halton.huo@sun.com
- Bump to 0.2.0
* Fri Jul 27 2007 - halton.huo@sun.com
- Initial spec file
