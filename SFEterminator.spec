#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEterminator
Summary:             Terminator - Multiple terminals in one window
Version:             0.9
Source:              http://launchpad.net/terminator/trunk/%{version}/+download/terminator_%{version}.tar.gz
URL:                 https://launchpad.net/terminator

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}_%{version}-build
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWPython
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-python-libs
Requires: SUNWPython

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%define pythonver 2.4

%prep
%setup -q -n terminator-%version

%build

python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix=$RPM_BUILD_ROOT%{_prefix}
mv %{buildroot}%{_libdir}/python%{pythonver}/site-packages \
  %{buildroot}%{_libdir}/python%{pythonver}/vendor-packages

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

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
%{_bindir}/terminator
%dir %attr(-,root,bin) %{_libdir}
%dir %attr(-,root,bin) %{_libdir}/python%{pythonver}
%dir %attr(-,root,bin) %{_libdir}/python%{pythonver}/vendor-packages
%{_libdir}/python%{pythonver}/vendor-packages/terminatorlib/*
%dir %attr(0755,root,sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/terminator.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%{_datadir}/icons/hicolor/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(-,root,bin) %{_mandir}/man5
%{_mandir}/man5/*

%changelog
* Wed Aug 06 2008 - (andras.barna@gmail.com)
- version bump
* Tue Jul 01 2008 - (andras.barna@gmail.com)
- Permission fixes
* Fri Jun 27 2008 - (andras.barna@gmail.com)
- Initial spec
