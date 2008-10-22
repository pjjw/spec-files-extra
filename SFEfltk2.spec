#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_name     fltk

Name:                SFEfltk2
Summary:             A C++ user interface toolkit
Version:             2.0.x-r6403
Source:              ftp://ftp.easysw.com/pub/fltk/snapshots/fltk-%{version}.tar.bz2
Patch1:		     fltk2-01-scandir.diff
Patch2:		     fltk2-02-lX11.diff
Patch3:		     fltk2-03-test.diff
Patch4:		     fltk2-04-fltk2-config.diff
Patch5:		     fltk2-05-destdir.diff
Patch6:		     fltk2-06-install.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWxwplt
Requires: SUNWxwplt

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%prep
%setup -q -n fltk-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
SFWLIB="-L/usr/SFW/lib -R/usr/SFW/lib"
GNULIB="-L/usr/gnu/lib -R/usr/gnu/lib"

export CFLAGS="%optflags -I/usr/X11/include -I/usr/gnu/include"
export LDFLAGS="%{_ldflags} $X11LIB $GNULIB"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/lib*.*a

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/man/cat*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/fluid2
%{_libdir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/fltk2-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Oct 22 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Bump to 6403
* Sat Jan 11 2008 - moinak.ghosh@sun.com
- Bump version, fix download URL
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial spec
