#
# spec file for package gnucash
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#


Name:           gnucash
Summary:        GnuCash is an application to keep track of your finances.
License:        GPL
Group:          Office
Version:        2.2.5
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.gnucash.org/
Source:         http://www.gnucash.org/pub/gnucash/sources/stable/%{name}-%{version}.tar.gz
# date:2008-06-24 owner:halton type:bug bugzilla:539947
Patch1:         %{name}-01-suncc-function.diff
# date:2008-06-24 owner:halton type:bug bugzilla:539962
Patch2:         %{name}-02-void-return.diff
# date:2008-06-24 owner:halton type:bug bugzilla:539957
Patch3:         %{name}-03-namely-struct.diff
# date:2008-06-25 owner:halton type:bug 
Patch4:         %{name}-04-inline.diff
# date:2008-06-25 owner:halton type:bug  bugzilla:540148
Patch5:         %{name}-05-libgoffice-0.8.diff
BuildRoot:      %{tmpdir}/%{name}-%{version}-root

Requires:       libgnomeui >= %{libgnomeui_version}
Requires:       libgnomeprintui22 >= %{libgnomeprintui22_version}
Requires:       guile >= %{guile_version}
Requires:       gtkhtml3 >= %{gtkhtml3_version}
Requires:       slib >= 3a1

BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  libgnomeprintui22-devel >= %{libgnomeprintui22_version}
BuildRequires:  gtkhtml3-devel >= %{gtkhtml3_version}
BuildRequires:  bzip2-devel, expat-devel, guile-devel
BuildRequires:  libglade2-devel, libgsf-devel
BuildRequires:  libjpeg-devel, openssl-devel


%description
GnuCash is a personal finance manager. A check-book like
register GUI allows you to enter and track bank accounts,
stocks, income and even currency trades. The interface is
designed to be simple and easy to use, but is backed with
double-entry accounting principles to ensure balanced books.

%package devel
Summary: Header files for GnuCash development.
Group: Development/Libraries
Requires: gnucash = %{version}

%description devel
This package contains header files for GnuCash development.
Install this package if you want to use GnuCash libraries
in C programs.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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

aclocal $ACLOCAL_FLAGS -I . -I macros
libtoolize --force
intltoolize --force --automake
autoheader
automake -a -f -c --gnu
autoconf

CFLAGS="$RPM_OPT_FLAGS"
./configure  --prefix=%{_prefix}         \
             --libdir=%{_libdir}         \
             --libexecdir=%{_libexecdir} \
             --datadir=%{_datadir}       \
             --mandir=%{_mandir}         \
             --sysconfdir=%{_sysconfdir} \
%if %debug_build
              --enable-debug             \
%endif
             --enable-gui


make -j $CPUS


%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/gnucash-design.info.gz %{_infodir}/dir

export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS=%{_sysconfdir}/gconf/schemas/apps_gnucash*.schemas
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule $S > /dev/null
done

%preun
if [ "$1" -eq 0 ]; then
     #deleting the schema on package removal
     export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
     SCHEMAS=%{_sysconfdir}/gconf/schemas/apps_gnucash*.schemas
     for S in $SCHEMAS; do
       gconftool-2 --makefile-uninstall-rule $S > /dev/null
     done
fi

%postun
/sbin/ldconfig
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/gnucash-design.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog* DOCUMENTERS HACKING LICENSE NEWS README
%doc doc/README.german doc/README.francais doc/guile-hackers.txt
%doc README ChangeLog AUTHORS NEWS
%attr(555,root,root) %{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/gnucash*info*
%{_libdir}/*
%{_datadir}/gnucash
%{_datadir}/applications/*
%{_datadir}/xml/gnucash/xsl/*
%{_datadir}/pixmaps/*
%{_sysconfdir}/gconf/schemas/apps_gnucash*
%config %{_sysconfdir}/gnucash

%files devel
%defattr(-,root,root)
%{_includedir}/gnucash

%changelog
* Wed Jun 25 2008 - nonsea@users.sourceforge.net
- Add inline.diff to fix ss11/ss12 build problem.
- Add libgoffice-0.8.diff to fix on latest goffice 0.7.0.
* Tue Jun 24 2008 - nonsea@users.sourceforge.net
- Add patch suncc-function.diff, void-return.diff
  namely-struct.diff
* Tue Jun 24 2008 - nonsea@users.sourceforge.net
- Add enable-debug option
* Thu Jan 19 2008 - nonsea@users.sourceforge.net
- Bump to 2.2.5
- Initial version
