#
# spec file for package SFElibmcrypt
#
# includes module(s): libmcrypt
#

Name:         SFElibmcrypt
Summary:      libmcrypt, replacement for Unix crypt under the GPL plus more algorithms and modes.
License:      Other
Group:        System/Libraries
Version:      2.5.8
Source:       %{sf_download}/mcrypt/libmcrypt-%{version}.tar.bz2
Url:          http://sourceforge.net/projects/mcrypt
Autoreqprov:  on

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            %{_basedir}
                           
%package devel             
Summary:                 %{summary} - developer files
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
Requires:                %{name}
%endif


%prep
rm -rf %name-%version
%setup -q -n libmcrypt-%version

%build
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} \
        	--enable-rpath                      \
            %{?configure_options}


make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
#%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
#%{_libdir}/pkgconfig/*


%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*



%changelog
* Sun Mar 18 2007 - Thomas Wagner
- Initial spec
