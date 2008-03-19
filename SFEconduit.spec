#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%define python_version 2.4

%include Solaris.inc

%use conduit = conduit.spec

Name:           SFEconduit
Summary:        %{conduit.summary}
Version:        %{default_pkg_version}
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:       SUNWbash
Requires:       SUNWgnome-base-libs
Requires:       SUNWPython
Requires:       SUNWsqlite3
Requires:       SUNWpysqlite
Requires:       SFEpython-dateutil
Requires:       SFEpython-vobject
Requires:       SFEpygoocanvas
BuildRequires:  SUNWgnome-base-libs-devel
BuildRequires:  SUNWPython-devel
BuildRequires:  SFEpygoocanvas-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%conduit.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export RPM_OPT_FLAGS="$CFLAGS"
%conduit.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%conduit.install -d %name-%version

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/conduit/[a-z][a-z]
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/conduit/[a-z][a-z]_[A-Z][A-Z]
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/conduit/conduit-[a-z][a-z].omf
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/conduit/conduit-[a-z][a-z]_[A-Z]*.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/conduit
%{_libdir}/python%{python_version}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/conduit
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, other) %{_datadir}/gnome
%dir %attr (0755, root, bin) %{_datadir}/gnome/autostart
%{_datadir}/gnome/autostart/*.desktop
%dir %attr (0755, root, bin) %{_datadir}/gnome/help
%{_datadir}/gnome/help/conduit*/C
%dir %attr (0755, root, bin) %{_datadir}/omf
%{_datadir}/omf/conduit/conduit*C.omf
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/*.service
%defattr (-, root, other)
%{_datadir}/icons

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, bin) %{_datadir}/omf
%{_datadir}/omf/conduit/conduit-[a-z][a-z].omf
%{_datadir}/omf/conduit/conduit-[a-z][a-z]_[A-Z][A-Z].omf
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/conduit/[a-z][a-z]
%{_datadir}/gnome/help/conduit/[a-z][a-z]_[A-Z][A-Z]
%endif

%changelog
* Fri Feb 22 2007 - jijun.yu@sun.com
- Modify the requires from SUNWpysqlite to SFEpysqlite
* Mon Feb 18 2007 - nonsea@users.sourceforge.net
- Add Requires: SUNWpysqlite
* Tue Dec 11 2007 - nonsea@users.sourceforge.net
- Initial spec
