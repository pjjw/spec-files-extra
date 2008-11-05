#
# spec file for package SFElibmhash
#
# includes module(s): libmhash
#
%include Solaris.inc

Name:         SFElibmhash
Summary:      Libmhash - uniform interface to several hash algorithms
License:      Other
Group:        System/Libraries
Version:      0.9.9
Source:       %{sf_download}/mhash/mhash-%{version}.tar.bz2
Url:          http://mhash.sf.net/ 
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

%include default-depend.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libmhash64 = libmhash.spec
%endif
%include base.inc
%use libmhash = libmhash.spec

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
%libmhash64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libmhash.prep -d %name-%version/%{base_arch}

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
%libmhash64.build -d %name-%version/%_arch64
%endif

%include base.inc
export CFLAGS="%optflags -features=extensions -D__const=const"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
%libmhash.build -d %name-%version/%{base_arch}

%install
%ifarch amd64 sparcv9
%libmhash64.install -d %name-%version/%_arch64
%endif

%libmhash.install -d %name-%version/%{base_arch}

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
#%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
%ifarch amd64 sparcv9
#%{_bindir}/%_arch64/*
%{_libdir}/%_arch64/*.so*
%endif

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.a*
%{_libdir}/*.la*
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/aclocal
#%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*
%ifarch amd64 sparcv9
%{_libdir}/%_arch64/*.a*
%{_libdir}/%_arch64/*.la*
%endif


%changelog
* Wed Nov 05 2008 - Michal Bielicki
- added 64bit version
- bumped up to 0.9.9
- moved to sunstudio
* Sun Mar 18 2007 - Thomas Wagner
- Initial spec
