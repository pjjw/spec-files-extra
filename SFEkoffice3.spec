#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define kde_version 3.5.8

Name:                SFEkoffice3
Summary:             KDE Office Suite Base Workspace
Version:             1.6.3
Source:              http://mirrors.isc.org/pub/kde/stable/koffice-%{version}/src/koffice-%{version}.tar.bz2
Patch1:              koffice-01-krita.diff
Patch2:              koffice-02-kross.diff
Patch3:              koffice-03-kspread.diff
Patch4:              koffice-04-objects.diff
Patch5:              koffice-05-libart.diff
Patch6:              koffice-06-build_kexi_file.diff

Source1:             koffice.files
Source2:             kexi.files
Source3:             kivio.files
Source4:             kplato.files
Source5:             krita.files
Source6:             kugar.files
Source7:             kchart.files
Source8:             kformula.files
Source9:             karbon14.files
Source10:            kpresenter.files
Source11:            kspread.files
Source12:            kword.files

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%include perl-depend.inc

# This also brings in all relevenat deps including kdelibs, qt, aRts and others.
Requires: SFEkdebase3
BuildRequires: SFEkdebase3-devel
Requires: SFEdoxygen
Requires: SFEwv2
BuildRequires: SFEwv2-devel
Requires: SFEwpd
BuildRequires: SFEwpd-devel
Requires: SUNWPython
BuildRequires: SUNWPython
BuildRequires: SUNWpostgr-devel
BuildRequires: SUNWmysqlu
Requires: SFElcms
BuildRequires: SFElcms-devel
Requires: SUNWlibexif
BuildRequires: SUNWlibexif-devel
Requires: SFEgraphviz
BuildRequires: SFEgraphviz-devel
Requires: SUNWimagick
BuildRequires: SUNWimagick
Requires: SUNWruby18u
BuildRequires: SUNWruby18u
Requires: SFEgraphicsmagick
BuildRequires: SFEgraphicsmagick-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEkdebase3-devel
Requires: SFEwv2-devel
Requires: SFEwpd-devel
Requires: SUNWPython
Requires: SUNWpostgr-devel
Requires: SUNWmysqlu
Requires: SFElcms-devel
Requires: SUNWlibexif-devel
Requires: SFEgraphviz-devel
Requires: SUNWimagick

%package kword
Summary:        A frame-based word processor in KOffice suite
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package kspread
Summary:        A powerful spreadsheet application in KOffice suite
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package kpresenter
Summary:        A full-featured presentation program in KOffice suite
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package kexi
Summary:        An integrated environment for databases and database applications in KOffice suite
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package kivio
Summary:        A Visio(R)-style flowcharting application in KOffice suite
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package karbon14
Summary:        A vector drawing application in KOffice suite
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package krita
Summary:        A layered pixel image manipulation application in KOffice suite
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package kplato
Summary:        An integrated project management and planning tool in KOffice suite
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package kchart
Summary:        An integrated graph and chart drawing tool in KOffice suite
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package kformula
Summary:        A powerful formula editor in KOffice suite
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package kugar
Summary:        A tool for generating business quality reports in KOffice suite
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n koffice-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

if [ "x`basename $CC`" != xgcc ]
then
	%error This spec file requires Gcc, set the CC and CXX env variables
fi

%build
%define _buildpath %{_builddir}/koffice-%version

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -fPIC -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} `/usr/bin/libart2-config --cflags` -D__EXTENSIONS__ -D__C99FEATURES__"

export CXXFLAGS="%cxx_optflags -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} `/usr/bin/libart2-config --cflags` -D__EXTENSIONS__ -D__C99FEATURES__"

export LDFLAGS="%_ldflags %{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path} -lc -lsocket -lnsl `/usr/bin/libart2-config --libs`"

export LIBS=$LDFLAGS

export PATH="${PATH}:/usr/openwin/bin"
export FREETYPE_CONFIG=%{sfw_bin}/freetype-config
extra_inc="%{xorg_inc}:%{gnu_inc}:%{sfw_inc}"
sfw_prefix=`dirname %{sfw_bin}`
export RUBY=/usr/ruby/1.8/bin/ruby

./configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --enable-final \
           --with-extra-includes="${extra_inc}" \
           --with-ssl-dir="${sfw_prefix}"


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# KDE requires the .la files
cp %{SOURCE1}  %{_buildpath}
cp %{SOURCE2}  %{_buildpath}
cp %{SOURCE3}  %{_buildpath}
cp %{SOURCE4}  %{_buildpath}
cp %{SOURCE5}  %{_buildpath}
cp %{SOURCE6}  %{_buildpath}
cp %{SOURCE7}  %{_buildpath}
cp %{SOURCE8}  %{_buildpath}
cp %{SOURCE9}  %{_buildpath}
cp %{SOURCE10} %{_buildpath}
cp %{SOURCE11} %{_buildpath}
cp %{SOURCE12} %{_buildpath}

export EPATT="karbon|chart|exi|kformula|kivio|plato|presenter|krita|kspread|kugar|kudes|kword"
(cd ${RPM_BUILD_ROOT}; \
    echo "%defattr (-, root, bin)" >> %{_buildpath}/koffice.files; \
    find ./%{_bindir} ./%{_libdir} \( -type f -o -type l \) | \
    egrep -v "$EPATT" | \
    sed 's/^\.\///' >> %{_buildpath}/koffice.files)

(cd ${RPM_BUILD_ROOT}; \
    echo "%defattr (-, root, other)" >> %{_buildpath}/koffice.files; \
    find ./%{_datadir} \( -type f -o -type l \) | \
    egrep -v "$EPATT" | \
    sed 's/^\.\///' >> %{_buildpath}/koffice.files)

(cd ${RPM_BUILD_ROOT}; \
    find ./%{_datadir}/icons ./%{_datadir}/apps/koffice/icons \( -type f -o -type l \) | \
    egrep "$EPATT" | \
    sed 's/^\.\///' >> %{_buildpath}/koffice.files)


rm -rf ${RPM_BUILD_ROOT}%{_datadir}/doc/HTML/en/koffice-apidocs

%clean
rm -rf $RPM_BUILD_ROOT

%files -f koffice.files

%files kword -f kword.files

%files kspread -f kspread.files

%files kpresenter -f kpresenter.files

%files kexi -f kexi.files

%files kivio -f kivio.files

%files karbon14 -f karbon14.files

%files krita -f krita.files

%files kplato -f kplato.files

%files kchart -f kchart.files

%files kformula -f kformula.files

%files kugar -f kugar.files

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Jan 28 2008 - moinak.ghosh@sun.com
- Initial spec.
