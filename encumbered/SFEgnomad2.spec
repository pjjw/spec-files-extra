# =========================================================================== 
#                    Spec File for Geany
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	gnomad2
%define src_version	2.9.0
%define pkg_release	1

# %{_topdir} is by default set to RPM_BUILD_ROOT
# Default path for RPM_BUILD_ROOT is /var/tmp/pkgbuild-{username}
# Install the software here as part of package building steps

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	SFE%{src_name}
Summary:      	Gnomad2 is a GTK+ music manager for Creative Zen
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPLv2 license
Group:          Multimedia/Audio Manager
Source:         %{sf_download}/gnomad2/%{src_name}-%{version}.tar.gz
Requires: 	SFElibnjb
Requires:	SFElibid3tag
Requires:   SFElibnjb
BuildRequires:	SFElibid3tag-devel

#Patch:        	gnomad2-01-2.8.13_p1_LDADD.diff
%if %is_s10
Patch:        	gnomad2-02-2.9.0_p2_mkdtemp.diff
%endif
Vendor:       	Linus Walleij
URL:            http://gnomad2.sourceforge.net
Packager:     	Anil Gulecha, Indraneel RR
BuildRoot:	%{_tmppath}/%{src_name}-%{version}-build

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%description 
Gnomad2 is a GTK+ music manager and swiss army knife for the Creative Labs NOMAD
and Zen range plus the Dell DJ devices using the Portable Digital Entertainment (PDE) protocol. 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
%setup -q -n %{src_name}-%{version}
./configure --prefix=%{_prefix}

%if %is_s10
%patch0 -p 1
%endif

%build
make

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/*
%dir %attr (0755, root, other) %{_datadir}/application-registry
%{_datadir}/application-registry/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/locale/ca
%dir %attr (0755, root, other) %{_datadir}/locale/ca/LC_MESSAGES
%{_datadir}/locale/ca/LC_MESSAGES/gnomad2.mo
%dir %attr (0755, root, other) %{_datadir}/locale/de
%dir %attr (0755, root, other) %{_datadir}/locale/de/LC_MESSAGES
%{_datadir}/locale/de/LC_MESSAGES/gnomad2.mo
%dir %attr (0755, root, other) %{_datadir}/locale/es
%dir %attr (0755, root, other) %{_datadir}/locale/es/LC_MESSAGES
%{_datadir}/locale/es/LC_MESSAGES/gnomad2.mo
%dir %attr (0755, root, other) %{_datadir}/locale/fi
%dir %attr (0755, root, other) %{_datadir}/locale/fi/LC_MESSAGES
%{_datadir}/locale/fi/LC_MESSAGES/gnomad2.mo
%dir %attr (0755, root, other) %{_datadir}/locale/fr
%dir %attr (0755, root, other) %{_datadir}/locale/fr/LC_MESSAGES
%{_datadir}/locale/fr/LC_MESSAGES/gnomad2.mo
%dir %attr (0755, root, other) %{_datadir}/locale/it
%dir %attr (0755, root, other) %{_datadir}/locale/it/LC_MESSAGES
%{_datadir}/locale/it/LC_MESSAGES/gnomad2.mo
%dir %attr (0755, root, other) %{_datadir}/locale/nl
%dir %attr (0755, root, other) %{_datadir}/locale/nl/LC_MESSAGES
%{_datadir}/locale/nl/LC_MESSAGES/gnomad2.mo
%dir %attr (0755, root, other) %{_datadir}/locale/no
%dir %attr (0755, root, other) %{_datadir}/locale/no/LC_MESSAGES
%{_datadir}/locale/no/LC_MESSAGES/gnomad2.mo
%dir %attr (0755, root, other) %{_datadir}/locale/pl
%dir %attr (0755, root, other) %{_datadir}/locale/pl/LC_MESSAGES
%{_datadir}/locale/pl/LC_MESSAGES/gnomad2.mo
%dir %attr (0755, root, other) %{_datadir}/locale/sco
%dir %attr (0755, root, other) %{_datadir}/locale/sco/LC_MESSAGES
%{_datadir}/locale/sco/LC_MESSAGES/gnomad2.mo
%dir %attr (0755, root, other) %{_datadir}/locale/sv
%dir %attr (0755, root, other) %{_datadir}/locale/sv/LC_MESSAGES
%{_datadir}/locale/sv/LC_MESSAGES/gnomad2.mo
%endif

%changelog
* Sun Dec 30 2007 - markwright@internode.on.net
- Bump to 2.9.0.  mkdtemp patch for Solaris 10.
* 2007.Aug.11 - Anil Gulecha, Indraneel RR
- Initial spec.
