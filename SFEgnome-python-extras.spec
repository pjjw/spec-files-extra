#
# spec file for package SFEgnome-python-extras
#
# includes module(s): gnome-python-extras
#

%include Solaris.inc
Name:                    SFEgnome-python-extras
Summary:                 Python bindings GNOME
URL:                     http://ftp.gnome.org/pub/GNOME/sources/gnome-python-extras
Version:                 2.19.1
Source:                  http://ftp.gnome.org/pub/GNOME/sources/gnome-python-extras/2.19/gnome-python-extras-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n gnome-python-extras-%version

%build
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/gtk-2.0/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/pygtk/*
%{_datadir}/gtk-doc/*

%changelog
* Tue Jul 10 2007 - Brian Cameron <brian.cameron@sun.com>
- Bump to 2.19.1

* Fri Feb 9 2007 - Irene Huang <irene.huang@sun.com>
- created
