#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEdeluge
Summary:             Deluge - BitTorrent client
Version:             0.5.9.1
Source:              http://download.deluge-torrent.org/source/%{version}/deluge-%{version}.tar.gz
Patch1:              deluge-01-sunpro.diff
#Patch2:              deluge-02-path.diff
#Patch3:              deluge-03-sparsefile.diff
Patch4:              deluge-04-sockaddr.diff
URL:                 http://deluge-torrent.org/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWPython
BuildRequires: SUNWopenssl-include
BuildRequires: SFEboost-devel
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-python-libs
Requires: SUNWPython
Requires: SUNWopenssl-libraries
Requires: SUNWzlib
Requires: SFEboost
Requires: SUNWpython-xdg

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
%setup -q -n deluge-torrent-%version
%patch1 -p1
#%patch2 -p1
#%patch3 -p1
%patch4 -p1
rm "plugins/WebUi/lib/webpy022/Dependency-not-really part of webui.txt"
# patch prefix before building
ed -s src/common.py <<'/EOF/' >/dev/null
,s:@datadir@:%_prefix:
w
q
/EOF/

%build
# workaround for pycc being invoked instead of pyCC
export PYCC_CC="$CXX"
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D__EXTENSIONS__ -I/usr/sfw/include \
 -library=stlport4 -staticlib=stlport4 -mt \
 -norunpath -features=tmplife -features=tmplrefstatic"
export CFLAGS="$CXXFLAGS"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib \
 -library=stlport4 -staticlib=stlport4 -lCrun -mt \
 -lpthread -lm -lsocket -lnsl -lcrypto"
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix=$RPM_BUILD_ROOT%{_prefix}

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

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
%{_bindir}/deluge
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/deluge
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/deluge
%{_datadir}/deluge/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/deluge.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128/apps
%{_datadir}/icons/hicolor/128x128/apps/deluge.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/deluge.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/192x192
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/192x192/apps
%{_datadir}/icons/hicolor/192x192/apps/deluge.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/deluge.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/deluge.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/256x256
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/256x256/apps
%{_datadir}/icons/hicolor/256x256/apps/deluge.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/deluge.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/36x36
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/36x36/apps
%{_datadir}/icons/hicolor/36x36/apps/deluge.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/deluge.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/64x64
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/64x64/apps
%{_datadir}/icons/hicolor/64x64/apps/deluge.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/72x72
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/72x72/apps
%{_datadir}/icons/hicolor/72x72/apps/deluge.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/96x96
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/96x96/apps
%{_datadir}/icons/hicolor/96x96/apps/deluge.png

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Oct 2 2008 - markwright@internode.on.net
- Bump to 0.5.9.1, bump patch1
* Thu Mar 27 2008 - trisk@acm.jhu.edu
- Bump to 0.5.8.7, bump patch4
* Wed Mar 26 2008 - trisk@acm.jhu.edu
- Bump to 0.5.8.6, bump patch1, add patch4
* Tue Feb 26 2008 - markwright@internode.on.net
- Bump to 0.5.8.4.
* Mon Dec 31 2007 - markwright@internode.on.net
- Bump to 0.5.8, bump patch1, comment patch 2 and 3.
* Mon Sep 17 2007 - trisk@acm.jhu.edu
- Bump to 0.5.5
* Sun Sep 02 2007 - trisk@acm.jhu.edu
- Fix Studio patch, fix file allocation issue
* Fri Aug 31 2007 - trisk@acm.jhu.edu
- Initial spec
