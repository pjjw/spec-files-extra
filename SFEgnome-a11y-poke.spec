#
# spec file for package SFEgnome-a11y-poke
#
# includes module(s): at-poke

%include Solaris.inc

%use at_poke = at-poke.spec

Name:                    SFEgnome-a11y-poke
Summary:                 Accessibility support tool
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_prefix}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-a11y-libs-devel
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-libs
Requires: SUNWxwrtl
Requires: SUNWxwplt
Requires: SUNWxwice
Requires: SUNWlxml
Requires: SUNWzlib
Requires: SUNWmlib
Requires: SUNWlibms
Requires: SUNWlibmsr
Requires: SUNWlibpopt
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnome-vfs
Requires: SUNWgnome-a11y-libs

%prep
rm -rf %name-%version
mkdir %name-%version
%at_poke.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export MSGFMT="/usr/bin/msgfmt"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export LDFLAGS="%_ldflags -norunpath"
export CFLAGS="%optflags"
%at_poke.build -d %name-%version

%install
%at_poke.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/at-poke

%changelog
*
* Thu Dec 06 2007 - Li Yuan
- Initial spec by Damien
