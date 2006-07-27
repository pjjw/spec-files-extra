#
# spec file for package SFEgeckosdk
#
# includes module(s): geckosdk
#
%include Solaris.inc

Name:                    SFEgeckosdk
%define code_name  bonecho
Summary:                 geckosdk  - Mozilla Gecko SDK
Version:                 2.0
%define tarball_version alpha3
Source:                  http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{code_name}/%{tarball_version}/source/%{code_name}-%{tarball_version}-source.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWj5rt
Requires: SUNWgnome-base-libs
Requires: SUNWdtbas
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWxwrtl
BuildRequires: SUNWzip
BuildRequires: SUNWgtar
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-base-libs-devel

%prep
%setup -q -n mozilla

%build
export PKG_CONFIG_PATH=${_libdir}/pkgconfig:%{_pkg_config_path}
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="-z ignore -L%{_libdir} -L/usr/sfw/lib -R'\$\$ORIGIN:\$\$ORIGIN/..' -R%{_libdir}"
%ifarch sparc
export CFLAGS="-xO5 -xlibmil"
export CXXFLAGS="-norunpath -xO5 -xlibmil -xlibmopt -features=tmplife"
%else
export CFLAGS="-xO3 -xlibmil"
export CXXFLAGS="-norunpath -xO3 -xlibmil -xlibmopt -features=tmplife"
%endif

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-standalone-modules=xpcom \
            --enable-application=standalone  \
            --enable-default-toolkit=gtk2    \
            --disable-debug                  \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/aclocal

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/mozilla-*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/idl

%changelog
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFEeckosdk
- removed -devel subpkg, since this is all devel stuff
- removed -share subpkg because we're not doing that kind of split anymore
- changed to root:bin to follow other JDS pkgs.
- added dependencies
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
