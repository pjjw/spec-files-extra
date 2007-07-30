#
# spec file for package SFEdoxygen
#
# includes module(s): doxygen
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%use doxygen = doxygen.spec

Name:               SFEdoxygen
Summary:            Doxygen is a documentation system for various languages
Version:            %{doxygen.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir -p %name-%version
%doxygen.prep -d %name-%version

%build
%doxygen.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%doxygen.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}


%changelog
* Mon Jul 30 2007 - markwright@internode.on.net
- bump to 1.5.3, remove patch1 as already applied, bump patch3.
* Mon Apr  2 2007 - laca@sun.com
- initial version created
