#
# spec file for package SFElibopensync
#
# includes module(s): libopensync
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
#

%include Solaris.inc

%use libopensync = libopensync.spec

Name:               SFElibopensync
Summary:            OpenSync - libopensync - A data synchronization framework
Version:            %{libopensync.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#Source1:           %{name}-manpages-0.1.tar.gz

Requires: SUNWPython
Requires: SUNWgnome-base-libs
Requires: SUNWlxml
Requires: SUNWzlib
Requires: SUNWsqlite3
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFEcmake
BuildRequires: SFEcheck
BuildRequires: SFEswig
BuildRequires: SUNWsqlite3

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%libopensync.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
#PYTHON_VERSION=`python -V 2>&1 | awk '{print $2}' | awk -F\. '{print $1"."$2}'`
#export PYTHON_VERSION
%libopensync.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libopensync.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/opensync-1.0
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%dir %attr (0755, root, bin) %{_libdir}/python2.4/site-packages
%{_libdir}/python2.4/site-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/opensync-1.0

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue Jun 24 2008 - nonsea@users.sourceforge.net
- Add BuildRequires SFEswig 
* Thu Dec 20 2007 - jijun.yu@sun.com
- Change the diretory under %{_libdir} and %{_datadir} from
  opensync to opensync-1.0
* Mon Nov 05 2007 - jijun.yu@sun.com
- Add some files into the package.
* Wed Jun 06 2007 - nonsea@users.sourceforge.net
- Add BuildRequires SFEscons and SFEcheck
- Change %{_datadir} attr to root:sys
* Tue Jun 05 2007 - jijun.yu@sun.com
- Bump to version 0.30
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires/BuildRequries after check-deps.pl run.
* Tue Nov 14 2006 - halton.huo@sun.com
- initial version created
