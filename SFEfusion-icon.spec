#
# spec file for package SFEfusion-icon
####################################################################
# compizconfig-settings-manager(fusion-icon): A fully featured Python/GTK 
# based settings manager for the CompizConfig system.
####################################################################
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


%include Solaris.inc

%define src_name fusion-icon
%define src_version 13-12-07

Name:                    SFEfusion-icon
Summary:                 fusion-icon - simple tray icon for Compiz Fusion
Version:                 0.1-20071003
Source:			 http://www.gnome.org/~erwannc/compiz/%{src_name}-%{src_version}.tar.bz2	 
Patch1:			 fusion-icon-01-solaris-port.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
# add build and runtime dependencies here:
BuildRequires:	SUNWgnome-base-libs-devel
BuildRequires:	SUNWgnome-python-libs-devel
BuildRequires:	SUNWPython
Requires:	SUNWgnome-base-libs
Requires:	SUNWgnome-python-libs
Requires:	SUNWPython
%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n %{src_name}
%patch1 -p1

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%post
rm -f %{_datadir}/icons/hicolor/icon-theme.cache
/usr/bin/gtk-update-icon-cache  %{_datadir}/icons/hicolor/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/FusionIcon
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/fusion-icon.desktop
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*

%changelog
* Thu Nov 08 2007 - erwann@sun.com
- added solaris port patch
* Fri Nov 02 2007 - erwann@sun.com
- clean up post install and added icon-cache update
* Tue Oct 30 2007 - trisk@acm.jhu.edu
- Initial spec
