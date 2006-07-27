#
# spec file for package SFEhp-gc
#
# includes module(s): Hans-Boehm gc
#
%include Solaris.inc

Name:                    SFEhp-gc
Summary:                 Boehm-Demers-Weiser garbage collector for C/C++
Version:                 6.6
Source:                  http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc%{version}.tar.gz
URL:                     http://www.hpl.hp.com/personal/Hans_Boehm/gc/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWPython
Requires: SUNWgnome-libs

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q            -c -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
cd gc%{version}
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd gc%{version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

rm $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gc

%changelog
* Thu Jul  6 2006 - laca@sun.com
- rename to SFEhp-gc
- delete -share subpkg
- update file attributes
- delete unnecessary env variables
* Mon Jan 30 2006 - glynn.foster@sun.com
- Initial version
