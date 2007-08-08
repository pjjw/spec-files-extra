#
# spec file for package SFEgst-python
#
# includes module(s): gst-python
#

%include Solaris.inc
Name:                    SFEgst-python
Summary:                 Python bindings for the GStreamer streaming media framework
URL:                     http://gstreamer.freedesktop.org/src/gst-python/
Version:                 0.10.8
Source:                  http://gstreamer.freedesktop.org/src/gst-python/gst-python-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
BuildRequires:           SUNWgnome-media

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n gst-python-%version

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
%{_libdir}/python%{pythonver}/vendor-packages/gst-0.10/*
%{_libdir}/python%{pythonver}/vendor-packages/pygst.pth
%{_libdir}/python%{pythonver}/vendor-packages/pygst.py
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gst-python

%changelog
* Tue Aug 7 2007  - brian.cameron@sun.com
- Bump to 0.10.8
* Fri Feb 9 2007  - irene.huang@sun.com
- bump to 0.10.7
* Thu Jan 11 2007 - laca@sun.com
- bump to 0.10.6
* Mon Sep 11 2006 - laca@sun.com
- created
