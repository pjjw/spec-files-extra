#
# spec file for package SFElibfribidi.spec
#
# includes module(s): libfribidi
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%use fribidi = fribidi.spec

Name:                   SFElibfribidi
Summary:                %fribidi.summary
Version:                0.10.9
Source:                 http://fribidi.org/download/fribidi-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir -p %name-%version
%fribidi.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%fribidi.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%fribidi.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Oct 22 2007 - nonsea@users.sourceforge.net
- Spilit into fribidi.spec
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version
