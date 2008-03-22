#
# spec file for package SUNWlcms
#
# includes module(s): lcms
#

%define python_version 2.4

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
##FIXME##%define arch_ldadd -Wl,-znolazyload -Wl,-L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}
%use lcms64 = lcms.spec
%endif

%include base.inc
##FIXME## should Solaris.inc be re-included again?
%define opt_arch64  0
%use lcms = lcms.spec

Name:                    SUNWlcms
Summary:                 lcms  - Little ColorManagement System 32/64-bit
Version:                 %{lcms.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%lcms64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
#isaexec is missing here (python2.4 seems to not being fully isaexec equipped)
%lcms.prep -d %name-%version/%{base_arch}

%build

%ifarch amd64 sparcv9
%lcms64.build -d %name-%version/%_arch64
%endif

%lcms.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%lcms64.install -d %name-%version/%_arch64
%endif

%lcms.install -d %name-%version/%{base_arch}

#only binaries for %{base_isa} should stay here (other bld_arch(es) place nothing here)
#base-isa is i86 or sparc(?)
[ -d $RPM_BUILD_ROOT%{_prefix}/bin/%{base_isa} ] || mkdir $RPM_BUILD_ROOT%{_prefix}/bin/%{base_isa}
for file in  `ls -1 $RPM_BUILD_ROOT%{_prefix}/bin/`
 do 
    [ -f $RPM_BUILD_ROOT%{_prefix}/bin/$file -a -x $RPM_BUILD_ROOT%{_prefix}/bin/$file ] || continue
    echo "preparing isaexec for file: $RPM_BUILD_ROOT%{_prefix}/bin/$file"
    mv $RPM_BUILD_ROOT%{_prefix}/bin/$file $RPM_BUILD_ROOT%{_prefix}/bin/%{base_isa}/
    ln -s ../../usr/lib/isaexec $RPM_BUILD_ROOT%{_prefix}/bin/$file
 done

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%dir %attr (0755, root, bin) %{_bindir}/%{base_isa}
%{_bindir}/%{base_isa}/*
%hard %{_bindir}/tifficc
%hard %{_bindir}/icc2ps
%hard %{_bindir}/tiffdiff
%hard %{_bindir}/jpegicc
%hard %{_bindir}/icclink
%hard %{_bindir}/wtpt
%hard %{_bindir}/icctrans
%elseif
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/python%{python_version}/vendor-packages/*.so
%{_libdir}/python%{python_version}/vendor-packages/*.py
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so.*
%{_libdir}/%{_arch64}/lib*.so
%dir %attr (0755, root, other)  %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%dir %attr (0755, root, other)  %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Wed Mar 22 2008 - Thomas Wagner
- create 64bit spec, move old spec to base-spec/lcms.spec
