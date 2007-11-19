#
# spec file for package epiphany
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
Name:         epiphany
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.20.1
Release:      4
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME web browser
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.20/%{name}-%{version}.tar.bz2
Patch1:       epiphany-01-runpath.diff
Patch2:       epiphany-02-grep-q.diff
Patch3:       epiphany-03-solaris.diff
Patch4:       epiphany-04-ns-headers.diff
URL:          http://www.gnome.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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
GECKO_CFLAGS="-I/usr/include/mps" GECKO_LIBS="-L/usr/lib/mps -R/usr/lib/mps -lnspr4 -lnss3 -lssl3 -lsoftokn3 -lsmime3 -lplds4 -lplc4 -lnssckbi -lfreebl3" CFLAGS="$RPM_OPT_FLAGS"	\
./configure --prefix=%{_prefix}		\
            --sysconfdir=%{_sysconfdir} \
            --libexecdir=%{_libexecdir} \
	    --enable-cpp-rtti \
            %{gtk_doc_option}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Nov 07 2007 - damien.carbery@sun.com
- Initial version.
