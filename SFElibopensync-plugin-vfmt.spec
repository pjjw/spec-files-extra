#
# spec file for package SFElibopensync-plugin-vfmt
#
# includes module(s): libopensync-plugin-vformat
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
#

%include Solaris.inc
%use vformat = libopensync-plugin-vfmt.spec

Name:               SFElibopensync-plugin-vfmt
Summary:            %vformat.summary
Version:            %{vformat.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SFElibopensync
BuildRequires: SUNWcmake
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFElibopensync-devel

%prep
rm -rf %name-%version
mkdir -p %name-%version
%vformat.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="-I%{_includedir} %optflags"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
export RPM_OPT_FLAGS="$CFLAGS"
%vformat.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%vformat.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Thu Jan 08 2009 - halton.huo@sun.com
- Use SUNWcmake
* Thu Sep 04 2008 - halton.huo@sun.com
- Use SFEcmake if cmake is not in $PATH
* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Remove -devel pkg
* Mon Aug 06 2007 - jijun.yu@sun.com
- Initial version.

