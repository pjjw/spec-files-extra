#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEexaile
Summary:             Music player for GTK+
Version:             0.2.13
Source:              http://www.exaile.org/files/exaile_%{version}.tar.gz
Patch1:              exaile-01-echodashe.diff
Patch2:              exaile-02-flump3dec.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# Requires:
BuildRequires: SFEgettext
Requires: SFEpython-mutagen

%prep
%setup -q -n exaile_%version
%patch1 -p0
%patch2 -p0

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

make PREFIX=%{_prefix} -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/%{_datadir}/locale/he_IL $RPM_BUILD_ROOT/%{_datadir}/locale/he
mv $RPM_BUILD_ROOT/%{_datadir}/locale/it_IT $RPM_BUILD_ROOT/%{_datadir}/locale/it
mv $RPM_BUILD_ROOT/%{_datadir}/locale/tr_TR $RPM_BUILD_ROOT/%{_datadir}/locale/tr


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/exaile/*
%dir %attr (0755, root, bin) %{_datadir}/man
%dir %attr (0755, root, bin) %{_datadir}/man/man1
%{_datadir}/man/man1/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/locale
%attr (-, root, other) %{_datadir}/locale/*

%changelog
* Tue Jun 24 2008 - river@wikimedia.org
- Initial spec
