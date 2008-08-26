#
# spec file for package SFExdelta
#
%include Solaris.inc
%define src_name xdelta

Name:                    SFExdelta
Summary:                 Opensource binary diff 
Group:                   Utility
Version:                 1.1.4
Source:                  http://xdelta.googlecode.com/files/%{src_name}-%{version}.tar.gz
URL:                     http://xdelta.org/
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{src_name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -mt -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_basedir}			\
            --bindir=%{_bindir}				\
            --datadir=%{_datadir}			\
            --mandir=%{_mandir}				\
            --libdir=%{_libdir}	

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%defattr (-, root, sys)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) /usr/include
/usr/include/*
%defattr (-, root, other)
%dir %attr (-, root, sys) %{_datadir}
%dir %attr (-, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%defattr (-, root, bin)
%dir %attr (-, root, bin) %{_mandir}
%dir %attr (-, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sun Jun 29 2008 - Petr Sobotka sobotkap@gmail.com
- Fixed build root directory.
* Wed May 07 2008 - Petr Sobotka sobotkap@centrum.cz
- Changed from development version to stable version
- for development version there will be soon SFExdelta3 spec file
* Thu Feb 14 2007 - Petr Sobotka sobotkap@centrum.cz
- Initial version
