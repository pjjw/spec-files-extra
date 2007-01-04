#
# spec file for package SFEbeagle
#
# includes module(s): beagle
#
%include Solaris.inc

Name:         SFEbeagle
Version:      0.2.9
Summary:      beagle - desktop search tool
Source:       http://ftp.gnome.org/pub/GNOME/sources/beagle/0.2/beagle-%{version}.tar.gz
URL:          http://beagle-project.org
Patch1:       beagle-01-solaris.diff
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
BuildRequires: SFEmono-devel
BuildRequires: SFEgtk-sharp
BuildRequires: SFEgmime-devel
BuildRequires: SFEsqlite-devel
Requires: %name-root
Requires: SFEmono
Requires: SFEgtk-sharp
Requires: SFEgmime
Requires: SFEsqlite

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:  /
%include default-depend.inc

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd beagle-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
cd beagle-%{version}

export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
		--mandir=%{_mandir} \
		--libdir=%{_libdir} \
		--libexecdir=%{_libexecdir} \
		--sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd beagle-%{version}
make DESTDIR=$RPM_BUILD_ROOT install

rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

for f in $RPM_BUILD_ROOT%{_bindir}/beagle* $RPM_BUILD_ROOT%{_sbindir}/beagle* \
    $RPM_BUILD_ROOT%{_libdir}/beagle/beagled-index-helper; do
    perl -pi -e 's/export BEAGLE_MONO_RUNTIME="mono"/export BEAGLE_MONO_RUNTIME="\/usr\/mono\/bin\/mono"/' $f
    perl -pi -e 's/exec -a (.*) mono /exec -a $1 \/usr\/mono\/bin\/mono /' $f
done

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/beagle
%{_libdir}/beagle/*
%{_libdir}/python*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/beagle
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Sep  7 2006 - jedy.wang@sun.com
- bump to 0.2.9
* Sun Jul 23 2006 - laca@sun.com
- rename to SFEbeagle
- add devel and l10n subpkgs
- update dependencies
* Wed Jul 13 2006 - jedy.wang@sun.com
- Initial spec
