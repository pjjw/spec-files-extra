#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#
%include Solaris.inc

Name:                    SFEgmp
Summary:                 GNU Multiple Presicion Arithmetic Library
Version:                 4.2.1
Source:                  ftp://ftp.gnu.org/gnu/gmp/gmp-%{version}.tar.bz2
URL:                     http://swox.com/gmp/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n gmp-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
export ABI=32
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --disable-cxx
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT%{_prefix}/info

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

%changelog
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEgmp
- bump to 4.2.1
- create devel subpkg
- update attributes
* Thu Nov 17 2005 - laca@sun.com
- create
