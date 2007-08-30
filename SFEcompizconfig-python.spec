#
# spec file for package SFEcompizconfig-python
####################################################################
# Python bindings for the compizconfig library
####################################################################
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


%include Solaris.inc

Name:                    SFEcompizconfig-python
Summary:                 compizconfig libraries - is an alternative configuration system for compiz
Version:                 0.5.2
Source:			 http://releases.compiz-fusion.org/0.5.2/compizconfig-python-%{version}.tar.bz2	 
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
# add build and runtime dependencies here:
BuildRequires:  SFElibcompizconfig
Requires:	SFElibcompizconfig

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
Requires:                %{name} = %{version}
%include default-depend.inc


%prep
%setup -q -c -n %name-%version

%build
cd compizconfig-python-%version
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

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
cd compizconfig-python-%version
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/python2.4/site-packages/*.*a
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
%{_libdir}/*

%files devel
%defattr (-, root, bin)
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
* Fri Aug  14 2007 - erwann@sun.com
- Initial spec
