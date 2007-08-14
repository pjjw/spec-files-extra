#
# spec file for package SFEccsm
####################################################################
# compizconfig-settings-manager(ccsm): A fully featured Python/GTK 
# based settings manager for the CompizConfig system.
####################################################################
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


%include Solaris.inc

Name:                    SFEccsm
Summary:                 ccsm settings manager for the CompizConfig system
Version:                 0.5.2
Source:			 http://releases.compiz-fusion.org/0.5.2/ccsm-%{version}.tar.bz2	 
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
# add build and runtime dependencies here:
BuildRequires:  SFEcompizconfig-python
Requires:	SFEcompizconfig-python
Requires:	%{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%prep
%setup -q -c -n %name-%version

%build
cd ccsm-%{version}
python setup.py build --prefix=%{_prefix}

%install
cd ccsm-%{version}
python setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

#
# when not building -l10n packages, remove anything l10n related from
# $RPM_BUILD_ROOT
#
%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files root
%defattr (0755, root, sys)
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/*
#
# The files included here should match the ones removed in %install
#
%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%changelog
* Fri Aug  14 2007 - erwann@sun.com
- Initial spec
