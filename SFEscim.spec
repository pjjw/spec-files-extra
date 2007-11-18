#
# spec file for package SFEscim
#
# includes module(s): scim
#
%include Solaris.inc

%define src_name scim
%define src_url http://switch.dl.sourceforge.net/sourceforge/%{src_name}

Summary:	Smart Common Input Method Framework
Name:		SFEscim
Version: 	1.4.7
Release:	1
License: 	LGPL
Group: 		System/GUI/GNOME
Source: 	%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		scim-01-ss11-patch.diff
Patch2:		scim-02-ss12-patch.diff
BuildRoot:      %{_tmppath}/%{cmpt}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-panel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-panel-devel
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-base-libs

%prep
%setup -q -n %{src_name}-%{version}

if [ -z "`cc -V 2>&1 | grep 5.9`" ]; then
  %patch1 -p1
else
  %patch2 -p1
fi

%build
export CFLAGS="%optflags"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
export CXXFLAGS="$CXXFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export LDFLAGS="-lsocket"
./bootstrap
./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --datadir=%{_datadir}		\
            --sysconfdir=%{_sysconfdir}         \
	    --disable-rpath			\
            --disable-debug
make

%install
rm -rf ${RPM_BUILD_ROOT}
DESTDIR=${RPM_BUILD_ROOT} make install
find ${RPM_BUILD_ROOT} -name "*.a" -exec rm  {} \; -print
find ${RPM_BUILD_ROOT} -name "*.la" -exec rm {} \; -print

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%post
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules

%clean
rm -rf ${RPM_BUILD_ROOT}

%files 
%defattr(-, root, bin)
%attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) /usr
%{_bindir}/*
%{_libdir}/lib*.so*
%{_libdir}/gtk-2.0/*
%{_libdir}/scim-1.0/*
%dir %attr (0755, root, sys) %{_datadir}
%attr (0755, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/control-center-2.0
%dir %attr (0755, root, other) %{_datadir}/control-center-2.0/capplets
%{_datadir}/control-center-2.0/capplets/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/scim/*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add support for building on Indiana systems.
* Thu Jul 26 2007 - dougs@truemail.co.th
- Initial spec, borrowed from opensolaris input-method project
