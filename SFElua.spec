#
# spec file for package lua scripting language
#
%include Solaris.inc
%define source_name lua

Name:                    SFElua
Summary:                 Lua - fast, simple scripting language
Version:                 5.1.2
Source:                  http://www.lua.org/ftp/%{source_name}-%{version}.tar.gz
URL:                     http://www.lua.org/
Patch1:                  lua-01-installdir.diff
Patch2:                  lua-02-suncc.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{source_name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{source_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

make solaris

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mv ${RPM_BUILD_ROOT}/usr/man ${RPM_BUILD_ROOT}/usr/share/man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (-, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/lua
%{_datadir}/lua/*

%changelog
* Tue Sep 11 2007 - Petr Sobotka sobotkap@centum.cz
- Initial version

