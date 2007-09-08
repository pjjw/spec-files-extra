#
# spec file for package SFEcompiz-fusion-main.spec
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
%include Solaris.inc

%define src_name compiz-fusion-plugins-main

Name:                    SFEcompiz-fusion-main
Summary:                 main effects plugins for compiz
Version:                 0.5.2
Source:			 http://releases.compiz-fusion.org/%{version}/%{src_name}-%{version}.tar.bz2
Patch1:			 compiz-fusion-main-01-solaris-port.diff
Patch2:                  compiz-fusion-main-02-sunpro.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEcompiz-bcop
BuildRequires: SFEcompiz-devel
Requires: SFEcompiz
# the base pkg should depend on the -root subpkg, if there is one:
Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:		 %summary - developer files
sUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%if %build_l10n
%package l10n
Summary:                 foo - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n %{src_name}-%version
%patch1 -p2
%patch2 -p1
# Ensure option code is regenerated by bcop XSLT
find . -name '*_options.c' -o -name '*_options.h' -exec rm -f {} \;

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

intltoolize --copy --force --automake
aclocal
autoheader
automake -a -c -f
autoconf

export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%{_ldflags}"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --includedir=%{_includedir}		\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
	    --enable-schemas 

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/compiz/*.la
rm $RPM_BUILD_ROOT%{_libdir}/compiz/*.a
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

%post root 
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/compiz-animation.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-colorfilter.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-expo.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-ezoom.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-imgjpeg.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-neg.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-opacify.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-put.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-resizeinfo.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-ring.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-snap.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-text.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-thumbnail.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-wall.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-winrules.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-workarounds.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-scaleaddon.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-vpswitch.schemas \
											   %{_sysconfdir}/gconf/schemas/compiz-shift.schemas

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/compiz
%{_libdir}/compiz/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/compiz
%{_datadir}/compiz/*

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%changelog
* Fri Sep 07 2007 - trisk@acm.jhu.edu
- Fix rules, add patch2
* Wed Aug 29 2007 - erwann@sun.com
- Initial spec