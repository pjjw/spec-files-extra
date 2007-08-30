#
# spec file for package SFEcompiz-fusion-extra.spec
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                    SFEcompiz-fusion-extra
Summary:                 extra effects plugins for compiz
Version:                 0.5.2
Source:			 http://releases.compiz-fusion.org/0.5.2/compiz-fusion-plugins-extra-%{version}.tar.bz2
Patch1:			 compiz-fusion-extra-01-solaris-port.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEcompiz-bcop
BuildRequires: SFEcompiz
BuildRequires: SFEcompiz-fusion-main
Requires: SFEcompiz
# the base pkg should depend on the -root subpkg, if there is one:
Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 foo - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
%patch1 -p1

%build
cd compiz-fusion-plugins-extra-%{version}
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
cd compiz-fusion-plugins-extra-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/compiz/*.la
rm $RPM_BUILD_ROOT%{_libdir}/compiz/*.a

%post root 
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule /etc/gconf/schemas/compiz-addhelper.schemas \
												/etc/gconf/schemas/compiz-bench.schemas \
												/etc/gconf/schemas/compiz-crashhandler.schemas \
												/etc/gconf/schemas/compiz-cubecaps.schemas \
												/etc/gconf/schemas/compiz-cubereflex.schemas \
												/etc/gconf/schemas/compiz-extrawm.schemas \
												/etc/gconf/schemas/compiz-fadedesktop.schemas \
												/etc/gconf/schemas/compiz-firepaint.schemas \
												/etc/gconf/schemas/compiz-gears.schemas \
												/etc/gconf/schemas/compiz-gotovp.schemas \
												/etc/gconf/schemas/compiz-group.schemas \
												/etc/gconf/schemas/compiz-mblur.schemas \
												/etc/gconf/schemas/compiz-reflex.schemas \
												/etc/gconf/schemas/compiz-scalefilter.schemas \
												/etc/gconf/schemas/compiz-showdesktop.schemas \
												/etc/gconf/schemas/compiz-splash.schemas \
												/etc/gconf/schemas/compiz-trailfocus.schemas \
												/etc/gconf/schemas/compiz-widget.schemas

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/*

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%changelog
* Wed Aug 29 2007 - erwann@sun.com
- Initial spec
