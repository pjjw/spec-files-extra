#
# spec file for package SFEsane-backends
#
# includes module(s): sane-backends
#
%include Solaris.inc
%use backends = sane-backends.spec

Name:                    SFEsane-backends
Summary:                 SANE - Scanner Access Now Easy - backends
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                %name-root
Requires:                SUNWlibusb
BuildRequires:           SUNWsfwhea

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
SUNW_BaseDir:            /

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%backends.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
# /usr/sfw needed for libusb
export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

%backends.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%backends.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT%{_sbindir}/
mv $RPM_BUILD_ROOT%{_prefix}/doc $RPM_BUILD_ROOT%{_datadir}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/sane
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/sane
%dir %attr(0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Mar 20 2007 - simon.zheng@sun.com
- Split into 2 files, SFEsane-backends.spec and
  linux-specs/sane-backends.spec

* Sun Nov  5 2006 - laca@sun.com
- Create
