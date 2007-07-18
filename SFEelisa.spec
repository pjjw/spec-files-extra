#
# spec file for package SFEelisa
#
# includes module(s): elisa
#
# Note that elisa does not run properly when you run the installed
# version.  You need to download elisa from SVN head and run the
# following command from the top-level directory to see elisa 
# working.
#
# python elisa.py sample_config/poblenou.conf
# 
# You may also need to add the following line to /etc/mime.types for
# the sample OGG files to be visible in elisa.
#
# application/ogg ogg
#
# Note that the 0.3.0.1 version is building "make dist" from SVN head.
# This latest version works on Solaris, whereas the last released version
# does not.  When 0.3.x actually comes out, then this will be a bit easier
# to build.  But for those who want to try out pigment right now, this
# spec file and instructions will let you get started working with the
# code.
#
%define name elisa
%define version 0.3.0.1

%include Solaris.inc

Name:              SFE%{name}
Summary:           Media center written in Python
URL:               http://elisa.fluendo.com/
Version:           %{version}
Source0:           http://elisa.fluendo.com/static/download/elisa/elisa-%{version}.tar.gz
Patch1:            elisa-01-solaris.diff
SUNW_BaseDir:      %{_basedir}
BuildRoot:         %{_tmppath}/%{name}-%{version}-build
BuildRequires:     SUNWPython-devel
BuildRequires:     SFEgnome-python-extras
BuildRequires:     SFEimagemagick
BuildRequires:     SFEpigment-devel
BuildRequires:     SFEpython-imaging
BuildRequires:     SFEpython-setuptools
BuildRequires:     SFEpython-twisted
BuildRequires:     SFEpysqlite
Requires:          SUNWgnome-media
Requires:          SUNWdbus-bindings
Requires:          SFEgnome-python-extras
Requires:          SFEimagemagick
Requires:          SFEpigment
Requires:          SFEpython-imaging
Requires:          SFEpython-setuptools
Requires:          SFEpython-twisted
Requires:          SFEpysqlite

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

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/elisa
%{_libdir}/python%{pythonver}/vendor-packages/elisa-%{version}-py%{pythonver}.egg-info

%changelog
* Tue Jul 10 2007 Brian Cameron  <brian.cameron@sun.com>
- Created spec.
