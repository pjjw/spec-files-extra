#
# spec file for package SFEfilezilla
#
# includes module(s): filezilla
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc
%use filezilla = filezilla.spec

Name:               SFEfilezilla
Summary:            FileZilla FTP client
Version:            %{filezilla.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-vfs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnutls
Requires: SUNWgnu-idn
Requires: SFEwxwidgets
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnutls-devel
BuildRequires: SUNWgnu-idn
BuildRequires: SFEwxwidgets-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%filezilla.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="-I%{_includedir} -I%{_includedir}/idn %optflags"
export CXXFLAGS="-I%{_includedir} -I%{_includedir}/idn"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
export RPM_OPT_FLAGS="$CFLAGS"
%filezilla.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%filezilla.install -d %name-%version

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
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/filezilla
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Thu Mar 06 2008 - nonsea@users.sourceforge.net
- Update %files cause version upgrade.
- Add pkg -l10n
- Repleace Requires/BuildRequires from SFElibidn to SUNWgnu-idn
* Mon Aug 06 2007 - nonsea@users.sourceforge.net
- initial version created
