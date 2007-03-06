#
# spec file for package SFEpitivi
#
# includes module(s): pitivi
#

%include Solaris.inc
Name:                    SFEpitivi
Summary:                 Non-Linear video editor
URL:                     http://ftp.gnome.org/pub/GNOME/sources/pitivi
Version:                 0.10.2
Source:                  http://ftp.gnome.org/pub/GNOME/sources/pitivi/0.10/pitivi-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:		 SFEgnonlin
BuildRequires:		 SFEgnome-python-extras
BuildRequires:		 SFEgst-python

%define         majmin          0.10

%include default-depend.inc

%prep
%setup -q -n pitivi-%version

%build
./configure --prefix=%{_prefix}	\
	    --enable-gstreamer
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_datadir}
%{_datadir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/pitivi

%changelog
* Fri Feb 9 2007  - irene.huang@sun.com
- created
