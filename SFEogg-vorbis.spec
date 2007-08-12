#
# spec file for package SUNWogg-vorbis.spec
#
# includes module(s): libogg, libvorbis
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libogg64 = libogg.spec
%use libvorbis64 = libvorbis.spec
%endif

%include base.inc
%use libogg = libogg.spec
%use libvorbis = libvorbis.spec

Name:                    SFEogg-vorbis
Summary:                 Ogg bitstream and Vorbis audio codec libraries
Version:                 %{default_pkg_version}
Source:                  SUNWogg-vorbis-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgnome-common-devel
BuildRequires: CBEbison
BuildRequires: SUNWPython
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libogg64.prep -d %name-%version/%_arch64
%libvorbis64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libogg.prep -d %name-%version/%{base_arch}
%libvorbis.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build

export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int

%ifarch amd64 sparcv9
%libogg64.build -d %name-%version/%_arch64
export PKG_CONFIG_PATH=%{_builddir}/%name-%version/%{_arch64}/libogg-%{libogg.version}:%{_pkg_config_path}
%libvorbis64.build -d %name-%version/%_arch64
unset PKG_CONFIG_PATH
%endif

%libogg.build -d %name-%version/%{base_arch}
export PKG_CONFIG_PATH=%{_builddir}/%name-%version/%{base_arch}/libogg-%{libogg.version}:%{_pkg_config_path}
%libvorbis.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libogg64.install -d %name-%version/%_arch64
%libvorbis64.install -d %name-%version/%_arch64
%endif

%libogg.install -d %name-%version/%{base_arch}
%libvorbis.install -d %name-%version/%{base_arch}

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
%ifarch amd64 sparcv9
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
%endif

# Only package 64bit related files
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.so*
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig
rm -rf $RPM_BUILD_ROOT%{_datadir}
rm -rf $RPM_BUILD_ROOT%{_includedir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
#%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
#%dir %attr (0755, root, other) %{_libdir}/pkgconfig
#%{_libdir}/pkgconfig/*
#%dir %attr (0755, root, bin) %{_includedir}
#%{_includedir}/*
#%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/aclocal
#%{_datadir}/aclocal/*
#%{_datadir}/gtk-doc
#%dir %attr(0755, root, bin) %{_mandir}
#%dir %attr(0755, root, bin) %{_mandir}/man3
#%{_mandir}/man3/*

%changelog
* Sun Aug 12 2007 - dougs@truemail.co.th
- copied from spec-files to provide 64bit libraries
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Mon Sep 12 2005 - laca@sun.com
- remove unpackaged files
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Thu Sep 09 2004 - matt.keenan@sun.com
- Added libogg.3, libvorbis.3 manpages
* Sat Jun 26 2004 - shirley.woo@sun.com
- changed install location to /usr/lib and /usr/bin
* Fri Jun 04 - brian.cameron@sun.com
- Initial spec-file created
