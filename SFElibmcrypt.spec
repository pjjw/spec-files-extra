#
# spec file for package SFElibmcrypt
#
# includes module(s): libmcrypt
#
%include Solaris.inc

Name:         SFElibmcrypt
Summary:      libmcrypt, replacement for Unix crypt under the GPL plus more algorithms and modes.
License:      Other
Group:        System/Libraries
Version:      2.5.8
Source:       %{sf_download}/mcrypt/libmcrypt-%{version}.tar.bz2
Url:          http://sourceforge.net/projects/mcrypt
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

%include default-depend.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libmcrypt64 = libmcrypt.spec
%endif
%include base.inc
%use libmcrypt = libmcrypt.spec

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc               
                           
%package devel             
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif


%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libmcrypt64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libmcrypt.prep -d %name-%version/%{base_arch}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
%ifarch amd64 sparcv9
%include arch64.inc
export CFLAGS="%optflags -m64 -features=extensions -D__const=const"
export LDFLAGS="%_ldflags -m64"
export RPM_OPT_FLAGS="$CFLAGS"
%libmcrypt64.build -d %name-%version/%_arch64
%endif

%include base.inc
export CFLAGS="%optflags -features=extensions -D__const=const"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
%libmcrypt.build -d %name-%version/%{base_arch}

%install
%ifarch amd64 sparcv9
%libmcrypt64.install -d %name-%version/%_arch64
#dir seemes to be empty
rmdir $RPM_BUILD_ROOT%{_libdir}/%_arch64/libmcrypt
%endif

%libmcrypt.install -d %name-%version/%{base_arch}
#dir seemes to be empty
rmdir $RPM_BUILD_ROOT%{_libdir}/libmcrypt


%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
#%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
#%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%{_libdir}/%_arch64/*.so*
%endif



%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.la*
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*
%ifarch amd64 sparcv9
%{_libdir}/%_arch64/*.la*
%endif


%changelog
* Wed Nov 05 2008 - Michal Bielicki
- added 64bit libs
- moved to SunStudio
* Sun Mar 18 2007 - Thomas Wagner
- Initial spec
