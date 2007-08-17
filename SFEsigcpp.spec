#
# spec file for package SFEsigcpp
#
# includes module(s): libsigc++
#
%include Solaris.inc

Name:                    SFEsigcpp
Summary:                 libsigc++ Typesafe Callback System for Standard C++
Version:                 2.0.17
URL:                     http://libsigc.sourceforge.net/
Source:                  http://ftp.gnome.org/pub/GNOME/sources/libsigc++/2.0/libsigc++-%{version}.tar.bz2
Patch1:                  sigcpp-01-build-fix.diff
Patch2:                  sigcpp-02-prototypes.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libsigc++-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
perl -pi -e 's/(\s*#define SIGC_TYPEDEF_REDEFINE_ALLOWED.*)/\/\/$1/' \
    sigc++/macros/signal.h.m4
%if %cc_is_gcc
export CXXFLAGS="%{gcc_cxx_optflags}"
%else
export CXX="${CXX} -norunpath"
export CXXFLAGS="%cxx_optflags -library=stlport4 -staticlib=stlport4 -features=tmplife -features=tmplrefstatic"
%endif
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} --disable-python
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/sigc++*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Add patch for missing prototypes in test
- Use stlport
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEsigcpp
- update permissions
* Fri May 05 2006 - damien.carbery@sun.com
- Bump to 2.0.17.
* Thu Nov 17 2005 - laca@sun.com
- add patch forte-workaround taken from
  http://bugzilla.gnome.org/show_bug.cgi?id=302098
* Wed Nov 16 2005 - laca@sun.com
- create
