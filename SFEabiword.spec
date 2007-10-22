#
# spec file for package SFEabiword
#
# includes module(s): abiword
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%use abiword = abiword.spec

Name:               SFEabiword
Summary:            %abiword.summary
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:           SUNWuiu8
Requires:           SUNWzlib
Requires:           SUNWgnome-base-libs
Requires:           SUNWpng
Requires:           SUNWlxml
Requires:           SUNWlibpopt
Requires:           SUNWaspell
Requires:           SUNWgnome-spell
Requires:           SUNWfontconfig
Requires:           SUNWperl584core
Requires:           SFElibfribidi
BuildRequires:      SUNWgnome-base-libs-devel
BuildRequires:      SUNWpng-devel
BuildRequires:      SUNWlxml-devel
BuildRequires:      SUNWlibpopt-devel
BuildRequires:      SUNWaspell-devel
BuildRequires:      SUNWgnome-spell-devel
BuildRequires:      SFElibfribidi-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}


%prep
rm -rf %name-%version
mkdir -p %name-%version
%abiword.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%abiword.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%abiword.install -d %name-%version
#mkdir -p $RPM_BUILD_ROOT%{_bindir}
#cp $RPM_BUILD_ROOT%{_prefix}/X11R6/bin/* $RPM_BUILD_ROOT%{_bindir}/
#rm -rf $RPM_BUILD_ROOT%{_prefix}/X11R6

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/abiword*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (-, root, other) %{_datadir}/icons
%{_datadir}/icons/*.png
%dir %attr (0755, root, other) %{_datadir}/mime-info
%{_datadir}/mime-info/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Wed Sep 26 2007 - nonsea@users.sourceforge.net
- Initial spec
