#
# spec file for package  SFEcompizconfig-backend-gconf
####################################################################
# The gconf backend for CompizConfig. It uses the Gnome configuration
# system and provides integration into the Gnome desktop environment.
####################################################################
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


%include Solaris.inc

%define src_name compizconfig-backend-gconf

Name:                    SFEcompizconfig-gconf
Summary:                 cgconf backend for CompizConfig
Version:                 0.5.2
Source:			 http://releases.compiz-fusion.org/%{version}/%{src_name}-%{version}.tar.bz2
Patch1:			 compizconfig-backend-gconf-01-solaris-port.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
# add build and runtime dependencies here:
BuildRequires:	SUNWgnome-base-libs-devel
BuildRequires:	SUNWgnome-libs-devel
BuildRequires:	SUNWgnome-config-devel
BuildRequires:  SFElibcompizconfig
Requires:	SUNWgnome-base-libs
Requires:	SUNWgnome-libs
Requires:	SUNWgnome-config
Requires:	SFElibcompizconfig

%prep
%setup -q -n %{src_name}-%version
%patch1 -p2

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

aclocal
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
            --libdir=%{_libdir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
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
%dir %attr (0755, root, bin) %{_libdir}/compizconfig
%{_libdir}/compizconfig/*

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
* Fri Sep 07 2007 - trisk@acm.jhu.edu
- Update rules
* Fri Aug  14 2007 - erwann@sun.com
- Initial spec
