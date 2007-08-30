#
# spec file for package SFEsexy-python.spec
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

####################################################################
# sexy-python is a set of Python bindings around libsexy
####################################################################

%include Solaris.inc

Name:                    SFEsexy-python
Summary:                 Python bindings around libsexy
Version:                 0.1.9
Source:			 http://releases.chipx86.com/libsexy/sexy-python/sexy-python-%{version}.tar.gz
Patch1:			 sexy-python-01-solaris-port.diff
URL:			 http://www.chipx86.com/wiki/Libsexy
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibsexy
Requires: SFElibsexy

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
cd sexy-python-%version
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
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}

make -j$CPUS

%install
cd sexy-python-%version
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/python2.4/site-packages/*.la

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
* Fri Aug  24 2007 - erwann@sun.com
- Initial spec
