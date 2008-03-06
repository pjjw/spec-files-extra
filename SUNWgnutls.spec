#
# spec file for package SUNWgnutls
#
# includes module(s): gnutls
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use gnutls64 = gnutls.spec
%endif

%include base.inc
%use gnutls = gnutls.spec

Name:          SUNWgnutls
Summary:       GNU transport layer security library
Version:       %{gnutls.version}
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWlibgcrypt
Requires:      SUNWzlib
Requires:      SUNWlibC

%package devel
%include default-depend.inc
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires: SUNWgnutls

%if %option_with_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%gnutls64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%gnutls.prep -d %name-%version/%base_arch

%build
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

%ifarch amd64 sparcv9
%gnutls64.build -d %name-%version/%_arch64
%endif

%gnutls.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%gnutls64.install -d %name-%version/%_arch64
rm -rf $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/psktool
%endif

%gnutls.install -d %name-%version/%base_arch
rm -rf $RPM_BUILD_ROOT%{_datadir}/man
rm -rf $RPM_BUILD_ROOT%{_datadir}/info
rm -rf $RPM_BUILD_ROOT%{_bindir}/psktool


%if %option_with_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT
%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gnutls*
%{_bindir}/certtool
%{_bindir}/srptool
%ifarch amd64 sparcv9
%{_bindir}/%{_arch64}/gnutls*
%{_bindir}/%{_arch64}/certtool
%{_bindir}/%{_arch64}/srptool
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/libgnutls-config
%{_bindir}/libgnutls-extra-config
%ifarch sparcv9 amd64
%{_bindir}/%{_arch64}/libgnutls-config
%{_bindir}/%{_arch64}/libgnutls-extra-config
%endif
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch sparcv9 amd64
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, bin) %{_datadir}/guile
%dir %attr (0755, root, bin) %{_datadir}/guile/site
%{_datadir}/guile/site/*

#FIXME: l10n build fails on nevada
%if %option_with_gnu_iconv
%if %option_with_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif
%endif

%changelog
* Thu Mar 06 2008 - nonsea@users.sourceforge.net
- Copied from spec-files for it is not allowed upgrade to 2.x
* Thu Apr 26 2007 - laca@sun.com
- set CXX to $CXX -norunpath because libtool swallows this option sometimes
  and leaves compiler paths in the binaries
* Thu Apr 05 2007 - damien.carbery@sun.com
- Remove code in %install that creates the libgnutls.so.12 symlink. The symlink
  was added as a workaround for 6519334 and is no longer needed. Removing the
  symlink fixes 6521160, a reminder bug to remove the symlink.
* Tue Mar 27 2007 - laca@sun.com
- enable 64-bit build
* Mon Feb  5 2007 - damien.carbery@sun.com
- Add Requires SUNWlibC after check-deps.pl run.
* Tue Jan 16 2007 - jedy.wang@sun.com
- Do not ship psktool right now.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 11 2006 - halton.huo@sun.com
- Change %defattr to (-, root, other).
* Thu May 04 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Tue Apr 04 2006 - halton.huo@sun.com
- Alter remove .a/.la files part into linux spec. 
* Thu Mar 30 2006 - halton.huo@sun.com
- Remove all *.a/*.la files.
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Wed Oct 26 2005 - <halton.huo@sun.com>
- ship files under /usr/bin to enable SSL in libsoup.
* Fri Sep 09 2005 - <laca@sun.com>
- remove unpackaged files or add to %files
* Wed Aug 31 2005 - halton.huo@sun.com
- Change SUNW_Category for open solaris
* Thu Jul 07 2005 - laca@sun.com
- define devel-share subpkg
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Tue Aug 31 2004 - shirley.woo@sun.com
- Bug 5091588 : include files should be in a separate devel package
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Thu Mar 11 2004 - <laca@sun.com>
- initial version created
