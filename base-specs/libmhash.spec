#
# spec file for package SFElibmhash
#
# includes module(s): libmhash
#

Name:         SFElibmhash
Summary:      Libmhash - uniform interface to several hash algorithms
License:      Other
Group:        System/Libraries
Version:      0.9.9
Source:       %{sf_download}/mhash/mhash-%{version}.tar.bz2
Url:          http://mhash.sf.net/ 

%package root
Summary:                 %{summary} - root
%include default-depend.inc               
                           
%package devel             
Summary:                 %{summary} - developer files
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
Requires:                %{name}
%endif


%prep
%setup -q -n mhash-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} 	\
            --enable-rpath                      \
            %{?configure_options}


make -j $CPUS

%install
make DESTDIR=${RPM_BUILD_ROOT} install

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
#%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*


%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/aclocal
#%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*



%changelog
* Sun Mar 18 2007 - Thomas Wagner
- Initial spec
