#
# spec file for package SUNWgmime
#
# includes module(s): gmime
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use gmime = gmime.spec

Name:          SUNWgmime
Version:       %{default_pkg_version}
Summary:       Libraries and binaries to parse and index mail messages
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
Requires:      SUNWzlib
Requires:      SUNWlibms
Requires:      SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
rm -rf %name-%version
mkdir %name-%version
%gmime.prep -d %name-%version

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%gmime.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gmime.install -d %name-%version

# conflicts with SUNWesu
rm -f $RPM_BUILD_ROOT%{_bindir}/uuencode
rm -f $RPM_BUILD_ROOT%{_bindir}/uudecode

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %dir %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.sh
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc
%endif

%changelog
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Remove mono stuff
- Add gtk-doc for %files devel
* Wed Jan 02 2008 - nonsea@users.sourceforge.net
- Rename from SFEgmime to SUNWgmime.
* Tue Jul 24 2007 - nonsea@users.sourceforge.net
- Bump to 2.2.10.
* Wed May  2 2007 - halton.huo@sun.com
- Bump to 2.2.8.
- Add check mono condition.
* Wed Sep  7 2006 - jedy.wang@sun.com
- bump to 2.2.3
* Sun Jul 13 2006 - laca@sun.com
- rename to SFEgmime
- include Solaris.inc
- correct patch file name, update CFLAGS, add gtk-docs to %files
* Wed Jul 12 2006 - jedy.wang@sun.com
- Initial spec
