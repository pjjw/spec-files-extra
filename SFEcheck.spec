#
# spec file for package SFEcheck
#
# includes module(s): check
#
%include Solaris.inc

Name:                    SFEcheck
Summary:                 Check - An unit testing framework for C
Version:                 0.9.5
Source:                  %{sf_download}/check/check-%{version}.tar.gz
Patch1:                  check-01-suncc-fail.diff
URL:                     http://check.sourceforge.net/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC

%prep
%setup -q -n check-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags"

./configure --prefix=%{_prefix}		    \
            --mandir=%{_mandir}             \
            --libdir=%{_libdir}             \
	    --enable-static=no

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_prefix}/info

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*.m4
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Mon Dec 15 2008 - halton.huo@sun.com
- Remove suncc-define.diff since SS12 support __attribute__
* Tue Mar 06 2007 - nonsea@users.sourceforge.net
- Initial spec file
