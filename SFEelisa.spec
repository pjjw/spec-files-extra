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
%define name elisa
%define version 0.3.5

%include Solaris.inc

Name:              SFE%{name}
Summary:           Media center written in Python
URL:               http://elisa.fluendo.com/
Version:           %{version}
Source0:           http://elisa.fluendo.com/static/download/elisa/elisa-%{version}.tar.gz
SUNW_BaseDir:      %{_basedir}
BuildRoot:         %{_tmppath}/%{name}-%{version}-build
BuildRequires:     SUNWPython-devel
BuildRequires:     SUNWPython-extra
BuildRequires:     SUNWimagick
BuildRequires:     SUNWsqlite3
BuildRequires:     SUNWpysqlite
BuildRequires:     SFEgnome-python-extras
BuildRequires:     SFEpigment-devel
BuildRequires:     SUNWpython-imaging
BuildRequires:     SUNWpython-setuptools
BuildRequires:     SUNWpython-twisted
BuildRequires:     SUNWpysqlite
BuildRequires:     SFEpigment-python
Requires:          SUNWPython
Requires:          SUNWPython-extra
Requires:          SUNWgnome-media
Requires:          SUNWdbus-bindings
Requires:          SUNWimagick
Requires:          SUNWsqlite3
Requires:          SUNWpysqlite
Requires:          SFEgnome-python-extras
Requires:          SFEpigment
Requires:          SUNWpython-imaging
Requires:          SUNWpython-setuptools
Requires:          SUNWpython-twisted
Requires:          SUNWpysqlite
Requires:          SFEpigment-python

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

%build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT

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
%{_libdir}/python%{pythonver}/vendor-packages/elisa-%{version}-py%{pythonver}.egg-info
%{_libdir}/python%{pythonver}/vendor-packages/elisa-%{version}-py%{pythonver}-nspkg.pth
%{_libdir}/python%{pythonver}/vendor-packages/elisa_generic_setup.py
%{_libdir}/python%{pythonver}/vendor-packages/elisa_generic_setup.pyc
%{_libdir}/python%{pythonver}/vendor-packages/elisa_plugin_core_setup.py
%{_libdir}/python%{pythonver}/vendor-packages/elisa_plugin_core_setup.pyc

%changelog
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
