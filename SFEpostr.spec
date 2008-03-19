#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEpostr
Summary:             Postr - upload photographs to Flickr
Version:             0.8
Source:              http://burtonini.com/computing/postr-%{version}.tar.gz
URL:                 http://burtonini.com/blog/computers/postr

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-file-mgr-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SUNWPython
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-file-mgr
Requires: SUNWgnome-python-libs
Requires: SUNWPython
Requires: SUNWpython-twisted

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n postr-%version

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix=$RPM_BUILD_ROOT/%_prefix

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/postr
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/postr.desktop
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/nautilus
%dir %attr (0755, root, bin) %{_libdir}/nautilus/extensions-1.0
%{_libdir}/nautilus/extensions-1.0/*
%{_libdir}/python%{pythonver}/vendor-packages/postr

%changelog
* Thu Aug 30 2007 - trisk@acm.jhu.edu
- Initial spec
