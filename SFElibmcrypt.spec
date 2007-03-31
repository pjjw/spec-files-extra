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
Source:       http://prdownloads.sourceforge.net/mcrypt/libmcrypt-%{version}.tar.bz2
Url:          http://sourceforge.net/projects/mcrypt
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

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
%setup -q -n libmcrypt-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la
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
