#
# spec file for package SUNWlibcdio
#
# includes module(s): libcdio
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Currently, libcdio doesn't work well on Solaris SPARC 
# because of endianess differences. A bug has been filed for it 
# at http://bugzilla.gnome.org/show_bug.cgi?id=377280. Patch
# has been provided as an workaround (please note that this
# is not a final solution). To make libcdio work on Solaris SPARC
# we suggest you applying the patch above.
%include Solaris.inc

%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)

%use libcdio = libcdio.spec

Name:                    SFElibcdio
Summary:                 GNU libcdio
Version:                 %{libcdio.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlexpt
Requires: SUNWlibC
Requires: SUNWlibmsr
Requires: SUNWgccruntime
Requires: SUNWlibms
Requires: SUNWdbus
Requires: SFElibcddb
Requires: SFElibiconv
Requires: SFEncurses
%if %with_hal
Requires: SUNWhal
%endif
BuildRequires: SUNWlexpt
BuildRequires: SUNWgcc
BuildRequires: SUNWdbus-devel
BuildRequires: SFElibcddb-devel
BuildRequires: SFElibiconv-devel
BuildRequires: SFEncurses-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%libcdio.prep -d %name-%version

# Note, we have to build this with gcc, because Forte cannot handle
# the flexible arrays used in libcdio.  We should move to using Forte
# if this issue is resolved with the Forte compiler.
#
%build
export CFLAGS="%gcc_optflags -I/usr/gnu/include -I/usr/gnu/include/ncurses"
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
%if %with_hal
export LDFLAGS="%_ldflags -lhal -ldbus-1 -R/usr/gnu/lib -L/usr/gnu/lib"
%else
export LDFLAGS="%_ldflags -R/usr/gnu/lib -L/usr/gnu/lib"
%endif

%libcdio.build -d %name-%version

%install
%libcdio.install -d %name-%version

#rm -rf $RPM_BUILD_ROOT%{_mandir}
#rm -rf $RPM_BUILD_ROOT%{_prefix}/share
#rm -rf $RPM_BUILD_ROOT%{_prefix}/info
rm -f $RPM_BUILD_ROOT%{_prefix}/share/info/dir

#%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/jp
%dir %attr (0755, root, bin) %{_mandir}/jp/man1
%{_mandir}/jp/man1/*
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/cdio

%changelog
* Wed Oct 22 2008 - dick@nagual.nl
- s/SUNWncurses/SFEncurses since the SUNpkg is not available
* Tue Sep 02 2008 - halton.huo@sun.com
- s/SFEncurses/SUNWncurses since it goes into vermillion
* Sun Aug 17 2008 - nonsea@users.sourceforge.net
- Add Requires/BuildRequires to SFEncurses and SFEncurses-devel
- Add -I/usr/gnu/include/ncurses in CFLAGS to fix build issue
- Move patches to libcdio.spec
* Fri Jul 11 2008 - andras.barna@gmail.com
- Add ACLOCAL_FLAGS, SFElibiconv dep, adjust ld+cflags
* Fri May 23 2008 - michal.bielicki <at> voiceworks.pl
- fix to manpath ownership
* Sat Jan 19 2008 - moinak.ghosh@sun.com
- Set g++ as cpp compiler
- Added back man and info files
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Changed reference to non-existent gcc_ldflags
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 0.79.  Add libcdio-02-stdint.diff.
* Thu Oct 18 2007 - laca@sun.com
- use gcc specific compiler/linker flags
* Mon Jun 23 - irene.huang@sun.com
- created.
