#
# spec file for package planner
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:			planner
License:		GPL
Group:			Applications/Office
Version:		0.13
Release:		2
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Planner, a project planning tool.
Source:			http://ftp.gnome.org/pub/GNOME/sources/planner/%{version}/planner-%{version}.tar.bz2
#FIXME: move from /usr/sfw/bin
Patch1:			planner-01-menu-entry.diff
Patch2:                 planner-02-forte-switches.diff
URL:			http://planner.imendio.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on

%define                 python_version                  2.4
%define			mrproject_version       	0.9.1
%define			glib2_version			2.4.0
%define			gtk2_version			2.0.4
%define			libgnomecanvas_version		2.6.0
%define			libgnomeui_version		2.6.0
%define			libglade_version		2.4.0
%define			libgnomeprintui_version		2.6.0
%define			gnome_vfs_version		2.6.0
%define			scrollkeeper_version		0.3.11
%define			libxml2_version         	2.4.7
%define			pygtk2_version			2.6.0

Requires:		libxml2			>=	%{libxml2_version}
Requires:		glib2			>=	%{glib2_version}
Requires:		gtk2			>=	%{gtk2_version}
Requires:		libgnomecanvas		>=	%{libgnomecanvas_version}
Requires:		libgnomeui		>=	%{libgnomeui_version}
Requires:		libglade		>=	%{libglade_version}
Requires:		libgnomeprintui		>=	%{libgnomeprintui_version}
Requires:		gnome-vfs		>=	%{gnome_vfs_version}
Requires:		pygtk2			>=	%{pygtk2_version}
Requires:               python                  >=      %{python_version}
BuildRequires:		libxml2-devel		>=	%{libxml2_version}
BuildRequires:		glib2-devel		>=	%{glib2_version}
BuildRequires:		gtk2-devel		>=	%{gtk2_version}
BuildRequires:		libgnomecanvas-devel	>=	%{libgnomecanvas_version}
BuildRequires:		libgnomeui-devel	>=	%{libgnomeui_version}
BuildRequires:		libglade-devel		>=	%{libglade_version}
BuildRequires:		libgnomeprintui-devel	>=	%{libgnomeprintui_version}
BuildRequires:		gnome-vfs-devel		>=	%{gnome_vfs_version}
BuildRequires:		pygtk2-devel		>=	%{pygtk2_version}
BuildRequires:		scrollkeeper		>=	%{scrollkeeper_version}
BuildRequires: 		shared-mime-info

Obsoletes:		mrproject		<=	%{mrproject_version}
Obsoletes:		libmrproject		<=	%{mrproject_version}
Provides:		mrproject		 =	%{mrproject_version}
Provides:		libmrproject		 =	%{mrproject_version}

%description
Planner is a tool for planning, scheduling and tracking projects. Planner is
an open source project targetting the GNOME Desktop.

%package devel
Summary:		Development headers and files for the planner libraries
Group:			Development/Libraries/X11
Autoreqprov:		on
Requires:		%{name} = %{version}
Requires:		libxml2-devel		>=	%{libxml2_version}
Requires:		glib2-devel		>=	%{glib2_version}
Requires:		gtk2-devel		>=	%{gtk2_version}
Requires:		libgnomecanvas-devel	>=	%{libgnomecanvas_version}
Requires:		libgnomeui-devel	>=	%{libgnomeui_version}
Requires:		libglade-devel		>=	%{libglade_version}
Requires:		libbonoboui-devel	>=	%{libbonoboui_version}
Requires:		libgnomeprintui-devel	>=	%{libgnomeprintui_version}
Requires:		gnome-vfs-devel		>=	%{gnome_vfs_version}

Obsoletes:		libmrproject-devel	<=	%{mrproject_version}
Provides:		libmrproject-devel	 =	%{mrproject_version}


%description devel
Planner is a tool for planning, scheduling and tracking projects. Planner is
an open source project targetting the GNOME Desktop. These files allow
developers to develop using Planner's features.

%prep
%setup -q
%patch1 -p1
%ifos solaris
%patch2 -p1
%endif


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

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
gtkdocize
autoheader
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}         \
	    --enable-gtk-doc            \
            --disable-update-mimedb     \
	    --sysconfdir=%{_sysconfdir}
./config.status
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
#clean up unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/file-modules/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/storage-modules/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/views/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime

rm -f $RPM_BUILD_ROOT%{_prefix}/lib/python*/site-packages/*/planner.la
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_prefix}/lib/python*/site-packages/* \
   $RPM_BUILD_ROOT%{_prefix}/lib/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_prefix}/lib/python*/site-packages

# Remove from yelp
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/planner

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/planner
%{_datadir}/application-registry/*
%{_datadir}/applications/*
%{_datadir}/gnome/help/planner/*
%{_datadir}/locale/*
%{_datadir}/mime-info/*
# Files removed from yelp.
# %{_datadir}/omf/planner/*
%{_datadir}/pixmaps/*
%{_datadir}/planner/*
%{_libdir}/planner/*/*.so
%{_libdir}/libplanner*.so
%{_libdir}/planner/*.so
%{_datadir}/doc/planner/*
%{_datadir}/icons
%{_sysconfdir}/gconf/schemas/planner.schemas

%files devel
%{_datadir}/gtk-doc/html/*
%{_includedir}/planner*/libplanner/*.h
%{_libdir}/pkgconfig/libplanner*.pc
%{_libdir}/libplanner*.so.*
%{_libdir}/python%{python_version}

%changelog
* Fri Dec 02 2005 - srirama.sharma@wipro.com
- Updated planner-01-menu-entry.diff to use the absolute path of the 
  executable in the .desktop file as usr/sfw/bin should not be 
  included in $PATH.
  Fixes bug #6345489.

* Tue Nov 29 2005 - laca.com
- remove javahelp stuff

* Thu Oct 27 2005 - laca@sun.com
- move the python stuff from site-packages to vendor-packages

* Thu Sep 01 2005 - damien.carbery@sun.com
- Add patch to remove compiler options that forte doesn't support.

* Fri Jul 01 2005 - matt.keenan@sun.com
- Add pkgconfig patch

* Wed Jun 29 2005 - damien.carbery@sun.com
- Remove '%{_datadir}/mime directory.

* Sat Jun 25 2005 - damien.carbery@sun.com
- Remove omf/planner dir from %files as the dir was removed during %install.

* Wed Jun 22 2005 - matt.keenan@sun.com
- Update l10n

* Wed Jun 08 2005 - glynn.foster@sun.com
- Bump to 0.13

* Tue May 25 2005 - brian.cameron@sun.com
- Fix build.

* Fri Feb 11 2005 - ghee.teo@sun.com
- Updated planner.spec to obsolete/provide the proper version of mrproject
  and libmrproject[-devel]. Fixes 6228278.

* Fri Jan 28 2005 - matt.keenan@sun.com
- #6222336 : Remove from yelp

* Thu Jan 20 2005 - alvaro.lopez@sun.com
- Added patch planner-06-save_as_crash.diff to fix bug #6219432

* Fri Nov 12 2004 - laca@sun.com
- Added --bindir and --libdir to configure opts so they can be redirected
  on Solaris

* Thu Oct 07 2004 - ciaran.mcdermott@sun.com
- Added planner-05-g11n-alllinguas.diff to add zh_TW locale

* Tue Oct 05 2004 - takao.fujiwara@sun.com
- Added planner-04-g11n-i18n-ui.diff to localize gnome-file-types-properties.
  Fixed 6173638

* Wed Sep 29 2004 - kaushal.kumar@wipro.com
- Added patch planner-03-fix-putenv-crash.diff.
  Fixes bug #5103739.

* Thu Aug 24 2004 - niall.power@sun.com
- added gtk-docs.

* Wed Jul 14 2004 - niall.power@sun.com
- fixed packaging for rpm4 and commented out
  "-j $CPUS" which is breaking the build.

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to planner-l10n-po-1.2.tar.bz2

* Thu Jul 08 2004 - dermot.mccluskey@sun.com
- undid -j $CPUS for this module

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to planner-l10n-po-1.2.tar.bz2

* Thu Jul 08 2004 - dermot.mccluskey@sun.com
- undid -j $CPUS for this module

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to planner-l10n-po-1.1.tar.bz2

* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris

* Thu Apr 01 2004 - matt.keenan@sun.com
- Javahelp conversion

* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar

* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding planner-l10n-po-1.0.tar.bz2 l10n content

* Thu Mar 11 2004 - yuriy.kuznetsov@sun.com
- added planner-02-g11n-potfiles.diff

* Tue Feb 24 2004 - michael.twomey@sun.com
- Initial package. Based on mrproject 0.9.1.
- Ported menu entry change, based on the mrproject patch.
