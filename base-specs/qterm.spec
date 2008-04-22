#
# spec file for package qterm
#
# includes module(s): qterm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton 
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=79581&atid=557094&aid=
#

Name:			qterm
Version:		0.5.1
Release:		1
License:		GPL
Group:			Development/Libraries
Distribution:           Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		BBS client based on Qt library
URL:			http://sourceforge.net/projects/qterm/
Source:			http://%{sf_mirror}/%{name}/%{name}-%{version}.tar.bz2
# date:2008-03-24 owner:halton type:bug bugid:1922334
Patch1:                 %{name}-01-allcoa.diff 
# date:2008-03-24 owner:halton type:bug bugid:1924060
Patch2:                 %{name}-02-nsl.diff 
BuildRoot:		%{_tmppath}/%{name}-%{version}-root

%description
QTerm is a BBS client

%package devel
Summary:		Header files, libraries and development documentation for %{name}
Group:			Development/Libraries
Requires:		%{name} = %{version}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

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

mkdir build && cd build
%if %debug_build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Debug ..
%else
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr ..
%endif

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
cd build
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%dir %{_datadir}/qterm

%changelog
* Mon Mar 24 2008 - nonsea@users.sourceforge.net
- Initial version
