#
# spec file for package poppler
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
# bugdb: bugzilla.freedesktop.org
#
Name:         poppler
License:      GPL
Group:        System/Libraries
Version:      0.6.2
Release:      1 
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      PDF Rendering Library
Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.gz
# date:2005-11-29 type:feature owner:laca bugzilla:9730
Patch1:       poppler-01-uninstalled.pc.diff
URL:          http://poppler.freedesktop.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}/%{name}
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define cairo_version 0.5.0
%define gtk2_version 2.4.0

Requires:      cairo >= %{cairo_version}
Requires:      gtk2 >= %{gtk2_version}

BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: gtk2-devel >= %{gtk2_version}

Obsoletes:     xpdf <= 3.0
Provides:      xpdf = 3.0

%description
Poppler is a fork of the xpdf PDF viewer developed by Derek Noonburg
of Glyph and Cog, LLC.  The purpose of forking xpdf is twofold.
First, we want to provide PDF rendering functionality as a shared
library, to centralize the maintenence effort.  Today a number of
applications incorporate the xpdf code base, and whenever a security
issue is discovered, all these applications exchange patches and put
out new releases.  In turn, all distributions must package and release
new version of these xpdf based viewers.  It's safe to say that
there's a lot of duplicated effort with the current situaion.  Even if
poppler in the short term introduces yet another xpdf derived code
base to the world, we hope that over time these applications will
adopt poppler.  After all, we only need one application to use poppler
to break even.

Second, we would like to move libpoppler forward in a number of areas
that doesn't fit within the goals of xpdf.  By design, xpdf depends on
very few libraries and runs a wide range of X based platforms.  This
is a strong feature and reasonable design goal.  However, with poppler
we would like to replace parts of xpdf that are now available as
standard components of modern Unix desktop environments.  One such
example is fontconfig, which solves the problem of matching and
locating fonts on the system, in a standardized and well understood
way.  Another example is cairo, which provides high quality 2D
rendering.

%package devel
Summary:      PDF Rendering Library
Group:        Development/Libraries
Requires:     %{name} = %{version}
Requires:     cairo-devel >= %{cairo_version}
Requires:     gtk2-devel >= %{gtk2_version}

%description devel
Poppler is a fork of the xpdf PDF viewer developed by Derek Noonburg
of Glyph and Cog, LLC.  The purpose of forking xpdf is twofold.
First, we want to provide PDF rendering functionality as a shared
library, to centralize the maintenence effort.  Today a number of
applications incorporate the xpdf code base, and whenever a security
issue is discovered, all these applications exchange patches and put
out new releases.  In turn, all distributions must package and release
new version of these xpdf based viewers.  It's safe to say that
there's a lot of duplicated effort with the current situaion.  Even if
poppler in the short term introduces yet another xpdf derived code
base to the world, we hope that over time these applications will
adopt poppler.  After all, we only need one application to use poppler
to break even.

Second, we would like to move libpoppler forward in a number of areas
that doesn't fit within the goals of xpdf.  By design, xpdf depends on
very few libraries and runs a wide range of X based platforms.  This
is a strong feature and reasonable design goal.  However, with poppler
we would like to replace parts of xpdf that are now available as
standard components of modern Unix desktop environments.  One such
example is fontconfig, which solves the problem of matching and
locating fonts on the system, in a standardized and well understood
way.  Another example is cairo, which provides high quality 2D
rendering.

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
aclocal $ACLOCAL_FLAGS -I . -I m4
autoheader
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --datadir=%{_datadir}       \
            --libdir=%{_cxx_libdir}     \
	    --sysconfdir=%{_sysconfdir} \
	    --enable-poppler-glib	\
            --disable-poppler-qt        \
            --disable-poppler-qt4       \
	    --mandir=%{_mandir}	        \
            --enable-zlib               \
            %{gtk_doc_option}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_cxx_libdir}/*.a
rm $RPM_BUILD_ROOT%{_cxx_libdir}/*.la
rm $RPM_BUILD_ROOT%{_bindir}/pdftoabw

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_bindir}
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-, root, root)
%{_includedir}/poppler/
%{_libdir}/*.so
%{_libdir}/pkgconfig/
%{_datadir}/gtk-doc

%changelog
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 0.6.2.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 0.6.1. Remove upstream patch, 02-fixcast.
* Mon Sep 03 2007 - brian.cameron@sun.com
- Bump to 0.6.0
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 0.5.91. Remove upstream patch, 02-c++issues.
* Wed Jul 04 2007 - darren.kenny@sun.com
- Remove poppler-02-glib-2.diff since it appears to be already in 0.5.9.
- Add new poppler-02-c++issues.diff patch to fix some C++ Compilation issues
  in 0.5.9.
* Fri May 18 2007 - laca@sun.com
- explicitely disable qt/qt4 support
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Sun Jun 11 2006 - laca@sun.com
- Bump to 0.5.3 to fix the build of evince
- Add patch, 03-glib-2, so that configure looks for glib-2.0, not the old glib.
  Freedesktop bugzilla #8600.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 0.5.1 as required by evince 0.5.2.
* Sun Jan 22 2006 - damien.carbery@sun.com
- Bump to 0.5.0, as required by evince 0.5.0.
- Point to 'm4' dir in aclocal call.
- Remove upstream patch, 01-freetype. Renumber others.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 0.4.4.
* Tue Jan 03 2006 - damien.carbery@sun.com
- Remove upstream patch, 02-macrofix.
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 0.4.3
* Tue Nov 29 2005 - laca@sun.com
- add uninstalled.pc.diff patch so that poppler can be in the same Solaris
  pkg as evince
* Thu Oct 13 2005 - damien.carbery@sun.com
- Enable poppler-glib as it is required by evince.
* Fri Sep 30 2005 - brian.cameron@sun.com
- Bump to 0.4.2
* Tue Sep 20 2005 - laca@sun.com
- add FREETYPE_CFLAGS to CFLAGS where needed
* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 0.4.0.
* Tue Aug 16 2005 - glynn.foster@sun.com
- Initial spec file for poppler
