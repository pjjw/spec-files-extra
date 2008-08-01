#
# spec file for package SFEelisa-plugins-bad
#
# includes module(s): elisa-plugins-bad
#
# bugdb: https://bugs.launchpad.net/elisa
#
%define name elisa-plugins-bad
%define version 0.5.3

%include Solaris.inc

Name:              SFE%{name}
Summary:           Bad plugins for Elisa
URL:               http://elisa.fluendo.com/
Version:           %{version}
Source0:           http://elisa.fluendo.com/static/download/elisa/elisa-plugins-bad-%{version}.tar.gz
SUNW_BaseDir:      %{_basedir}
BuildRoot:         %{_tmppath}/%{name}-%{version}-build
Requires:          SFEelisa
Requires:          SFEelisa-plugins-good

%include default-depend.inc

%define pythonver 2.4

%description
The Elisa bad plugins set contains plugins known to be working well but with
code needing more QA (unittests, code reviews).

%prep
%setup -q -n elisa-plugins-bad-%version

%build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages

mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

rm -f $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/elisa/plugins/__init__.py
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/elisa/plugins/__init__.pyc

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/elisa
%{_libdir}/python%{pythonver}/vendor-packages/elisa_plugin_*-nspkg.pth
%{_libdir}/python%{pythonver}/vendor-packages/elisa_plugin_*.egg-info

%changelog
* Thu Jul 31 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.5.3.  Remove patch that disabled onscreen since it is no
  longer needed.
* Wed Jul 23 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.5.2.  Add patch to disable onscreen plugin, since it fails
  due to xml.etree not being available.
* Wed Mar 19 2008 Brian Cameron  <brian.cameron@sun.com>
- Created spec.
