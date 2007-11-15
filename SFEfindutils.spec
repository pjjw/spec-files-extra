#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

# Relegating to /usr/gnu to avoid name collisions
%define _prefix %{_basedir}/gnu

Name:                SFEfindutils
Summary:             GNU find, locate, and xargs
Version:             4.2.31
URL:                 http://www.gnu.org/software/findutils/
Source:              http://ftp.gnu.org/pub/gnu/findutils/findutils-%{version}.tar.gz

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
%setup -q -n findutils-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -R/usr/gnu/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --infodir=%{_datadir}/info \
	    --libexecdir=%{_libexecdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rmdir $RPM_BUILD_ROOT%{_prefix}%{_localstatedir}
rm $RPM_BUILD_ROOT%{_prefix}/lib/charset.alias

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info
%{_mandir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Correct path to charset.alias file.
* Sun Oct 14 2007 - laca@sun.com
- fix l10n installation
* Tue Sep 18 2007 - nonsea@users.sourceforge.net
- Bump to 4.2.31
* Sun Sep 24 2006 - Eric Boutilier
- Initial spec
