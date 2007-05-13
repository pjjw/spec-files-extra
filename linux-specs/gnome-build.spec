#
# spec file for package gnome-build
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:		gnome-build
License:	GPL
Group:		Development/Libraries
Version:	0.1.6
Release:	1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:		http://www.gnome.org
Summary:	GNOME Build Framework.
Source:		http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.1/%{name}-%{version}.tar.bz2
# date:2007-03-28 owner:nonsea type:branding
Patch1:         %{name}-01-gnu-regex.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

Requires:	libglade >= 2.0.1
Requires:	gdl >= 0.7.0
BuildRequires:  gtk+-devel >= 2.3.0
BuildRequires:	libglade-devel >= 2.0.1
BuildRequires:	gdl-devel >= 0.7.0


%description
This is the GNOME Build Framework (GBF).

%package devel
Summary:	Libraries and include files for Gnome Build Framework.
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel 
Libraries and header files if you want to make use of the GNOME debug framework
in your own programs.


%prep
%setup -q
%patch1 -p1

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
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} \
    --bindir=%{_bindir} --mandir=%{_mandir} \
    --localstatedir=%{_localstatedir} --libdir=%{_libdir} \
    --datadir=%{_datadir} --includedir=%{_includedir} \
    --sysconfdir=%{_sysconfdir}

make # -j $CPUS

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{_prefix} bindir=$RPM_BUILD_ROOT%{_bindir} \
    mandir=$RPM_BUILD_ROOT%{_mandir} libdir=$RPM_BUILD_ROOT%{_libdir} \
    localstatedir=$RPM_BUILD_ROOT%{_localstatedir} \
    datadir=$RPM_BUILD_ROOT%{_datadir} \
    includedir=$RPM_BUILD_ROOT%{_includedir} \
    sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir} install

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS COPYING ChangeLog NEWS README
%defattr (-, root, root)
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_libdir}/gnome-build-1.0
%{_datadir}/pixmaps/*.png
%{_datadir}/gnome-build
%{_datadir}/locale

%files devel
%defattr (-, root, root)
%{_includedir}/gnome-build-1.0
%{_libdir}/*a
%{_libdir}/*so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sun May 13 2007 - nonsea@users.sourceforge.net
- Bump to 0.1.6.
- Remove upstreamed patch debug-define.diff.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Disabled parallel make. Can be a problem on a multicpu system
* Thu Apr 05 2007 - nonsea@users.sourceforge.net
- Remove patch share-glue.diff, since this problem
  is resolved in anjuta.
* Wed Apr 04 2007 - nonsea@users.sourceforge.net
- Add patch share-glue.diff.
* Thu Mar 29 2007 - nonsea@users.sourceforge.net
- Add bug comments.
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Initial spec
