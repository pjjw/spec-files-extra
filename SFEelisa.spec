#
# spec file for package SFEelisa
#
# includes module(s): elisa
#
# You may need to add the following line to /etc/mime.types for
# the sample OGG files to be visible in elisa.
#
# application/ogg ogg
#
# bugdb: https://bugs.launchpad.net/elisa
#
%define name elisa
%define version 0.5.15

%include Solaris.inc

Name:              SFE%{name}
Summary:           Media center written in Python
URL:               http://elisa.fluendo.com/
Version:           %{version}
Source0:           http://elisa.fluendo.com/static/download/elisa/elisa-%{version}.tar.gz
# See bug #249822.
Patch1:            elisa-01-fixlocale.diff
SUNW_BaseDir:      %{_basedir}
BuildRoot:         %{_tmppath}/%{name}-%{version}-build
BuildRequires:     SUNWPython-devel
BuildRequires:     SUNWPython-extra
BuildRequires:     SUNWimagick
BuildRequires:     SUNWsqlite3
BuildRequires:     SUNWpysqlite
BuildRequires:     SUNWgnome-python-extras
BuildRequires:     SUNWpysqlite
BuildRequires:     SFEpigment-devel
Requires:          SUNWPython
Requires:          SUNWPython-extra
Requires:          SUNWgnome-media
Requires:          SUNWdbus-bindings
Requires:          SUNWimagick
Requires:          SUNWsqlite3
Requires:          SUNWpysqlite
Requires:          SUNWgnome-python-extras
Requires:          SUNWpython-imaging
Requires:          SUNWpython-setuptools
Requires:          SUNWpython-twisted
Requires:          SUNWpysqlite
Requires:          SFEpyopenssl
Requires:          SFEpigment
Requires:          SFEpigment-python
Requires:          SFEpython-cssutils
Requires:          SFEpython-twisted-web2

%include default-depend.inc

%define pythonver 2.4

%description
Elisa is a project to create an open source cross platform media center 
solution. Elisa runs on top of the GStreamer multimedia framework and 
takes full advantage of harware acceleration provided by modern graphic 
cards by using OpenGL APIs. In addition to personal video recorder 
functionality (PVR) and Music Jukebox support, Elisa will also 
interoperate with devices following the DLNA standard like Intelâ??s ViiV 
systems.

%prep
%setup -q -n elisa-%version
%patch1 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
python2.4 setup.py install --root=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u


%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/elisa
%{_bindir}/elisa-get
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/elisa
%{_libdir}/python%{pythonver}/vendor-packages/elisa-*-py%{pythonver}.egg-info
%{_libdir}/python%{pythonver}/vendor-packages/elisa-*-py%{pythonver}-nspkg.pth
%{_libdir}/python%{pythonver}/vendor-packages/elisa_generic_setup.py
%{_libdir}/python%{pythonver}/vendor-packages/elisa_generic_setup.pyc

%changelog
* Tue Oct 21 2008 Jerry Yu <jijun.yu@sun.com>
- Bump to 0.5.15.
* Tue Oct 14 2008 Jerry Yu <jijun.yu@sun.com>
- Bump to 0.5.14. 
- Comment some unuseful commands.
* Mon Oct 13 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.5.13.  Remove upstream patch elisa-02-defaultdict.diff.
* Tue Sep 30 2008 Brian Cameron  <brian.cameron@sun.com
- Bump to 0.5.12.  Add patch  elisa-02-defaultdict.diff, so it no longer
  depends on Python 2.5 and works with 2.4.
* Thu Sep 25 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.5.11.
* Wed Sep 17 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.5.10.
* Sun Sep 07 2008 Brian Cameron  <brian.cameron@sun.com
- Bump to 0.5.8.
* Mon Aug 18 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.5.5.
* Sat Aug 09 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.5.4.  Remove upstream patch elisa-02-nohal.diff.
* Thu Jul 31 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.5.3.  Add patch to disable HAL for now.  It requires D-Bus
  system services to be enabled for detecting hotplugged volumes.  However,
  we don't support D-Bus system services now.
* Tue Jul 29 2008 Jerry Yu <jijun.yu@sun.com>
- Correct the dependency pkg name.
* Wed Jul 23 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.5.2.  Add patch to fix bug with locale code.  Refer to bug
  #249822.
* Mon Apr 07 2008 Brian Cameron  <brian.cameron@sun.com>
- Change SFEgnome-python-extras to SUNWgnome-python-extras.
* Wed Mar 19 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.5.
* Wed Jan 16 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.3.  Add SFEpigment-python as a new dependency.
* Thu Oct 25 2007 Brian Cameron  <brian.cameron@sun.com>
- Add SUNWPython-extra dependency since it depends on elementtree.
* Fri Oct 05 2007 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.2
* Sun Aug 05 2007 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.1
* Tue Jul 10 2007 Brian Cameron  <brian.cameron@sun.com>
- Created spec.
