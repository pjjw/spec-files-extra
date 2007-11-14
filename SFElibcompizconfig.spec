#
# spec file for package SFElibcompizconfig
####################################################################
# Libcompizconfig is an alternative configuration system for compiz
####################################################################
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


%include Solaris.inc

%define src_name libcompizconfig

Name:                    SFElibcompizconfig
Summary:                 compizconfig libraries - is an alternative configuration system for compiz
Version:                 0.6.0
Source:			 http://releases.compiz-fusion.org/%{version}/%{src_name}-%{version}.tar.bz2
Patch1:			 libcompizconfig-01-solaris-port.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
# add build and runtime dependencies here:
BuildRequires:  SFEcompiz
Requires:	SFEcompiz
# the base pkg should depend on the -root subpkg, if there is one:
Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
Requires:                %{name} = %{version}
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

aclocal
autoheader
automake -a -c -f
autoconf

export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%{_ldflags} -L/usr/X11/lib -L/usr/openwin/lib -R/usr/X11/lib -R/usr/openwin/lib -lX11 -lXext"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --includedir=%{_includedir}		\
            --libdir=%{_libdir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/compiz/*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/compizconfig/backends/*.*a

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
%{_libdir}/compiz
%{_libdir}/compizconfig
%{_libdir}/lib*.so*

%files root
%defattr (0755, root, sys)
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/*
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

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
* Wed Nov 14 2007 - daymobrew@users.sourceforge.net
- Add l10n package.
* Mon Oct 29 2007 - trisk@acm.jhu.edu
- Bump to 0.6.0
* Sat Sep 15 2007 - trisk@acm.jhu.edu
- Fix patch rule
* Sat Sep 08 2007 - trisk@acm.jhu.edu
- Update rules
* Fri Aug 31 2007 - trisk@acm.jhu.edu
- Fix duplicate package contents
* Fri Aug  14 2007 - erwann@sun.com
- Initial spec
