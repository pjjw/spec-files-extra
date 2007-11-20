#
# spec file for package SFEvnc2swf
#
# includes module(s): vnc2swf
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use vnc2swf = vnc2swf.spec

Name:               SFEvnc2swf
Summary:            %vnc2swf.summary
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SUNWlibC
Requires:           SUNWlibms
Requires:           SUNWxwrtl

%prep
rm -rf %name-%version
mkdir -p %name-%version
%vnc2swf.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%vnc2swf.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%vnc2swf.install -d %name-%version
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp $RPM_BUILD_ROOT%{_prefix}/X11R6/bin/* $RPM_BUILD_ROOT%{_bindir}/
rm -rf $RPM_BUILD_ROOT%{_prefix}/X11R6

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Mon Jul 30 2007 - nonsea@users.sourceforge.net
- Initial spec
