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

%define have_swig %(/usr/bin/pkginfo -q SUNWswig && echo 1 || echo 0)

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
BuildRequires: SFEcheck
BuildRequires: SUNWsqlite3
BuildRequires: SUNWcmake
%if %have_swig
BuildRequires: SUNWswig
%define python_version  2.4
%endif

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
%libopensync.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libopensync.install -d %name-%version

# move to vendor-packages
%if %have_swig
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libopensync1
%{_libdir}/*.so*
%if %have_swig
%{_libdir}/python%{python_version}/vendor-packages
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/libopensync1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/libopensync1
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Jan 08 2009 - halton.huo@sun.com
- Use SUNWcmake
* Mon Oct 20 2008 - halton.huo@sun.com
- swig integrate into snv_100, rename SFEswig to SUNWswig
* Thu Sep 04 2008 - halton.huo@sun.com
- Update %files cause version upgrade
- Use SFEcmake if cmake is not in $PATH
- Move SFEswig as optional depend
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
