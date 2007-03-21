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


%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n pitivi-%version

%build
./configure --prefix=%{_prefix}	\
	    --enable-gstreamer
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/pitivi
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/pitivi
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Wed Mar 21 2007 - daymobrew@users.sourceforge.net
- Add l10n package and correct file permissions.

* Fri Feb  9 2007  - irene.huang@sun.com
- created
