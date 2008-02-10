#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEsharutils
License:             GPL
Summary:             A utility to create self-extracting Shell Archives.
Version:             4.7
URL:                 http://www.gnu.org/software/sharutils/
Source:              ftp://ftp.gnu.org/gnu/sharutils/REL-%{version}/sharutils-%{version}.tar.bz2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n sharutils-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --enable-shared=yes \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
rm -rf ${RPM_BUILD_ROOT}%{_libdir}
rm -f ${RPM_BUILD_ROOT}%{_datadir}/info/dir
rm -f ${RPM_BUILD_ROOT}%{_bindir}/uudecode
rm -f ${RPM_BUILD_ROOT}%{_bindir}/uuencode
rm -f ${RPM_BUILD_ROOT}%{_datadir}/locale/locale.alias
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/uudecode.1
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/uuencode.1

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
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Feb 10 2008 - moinak.ghosh@sun.com
- Initial spec.
