#
# spec file for package SFEglibmm
#
# includes module(s): glibmm
#
%include Solaris.inc

Name:                    SFEglibmm
Summary:                 glibmm - C++ Wrapper for the Glib2 Library
Version:                 2.12.7
URL:                     http://www.gtkmm.org/
Source:                  http://ftp.acc.umu.se/pub/GNOME/sources/glibmm/2.12/glibmm-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEsigcpp
BuildRequires: SFEsigcpp-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel

%prep
%setup -q -n glibmm-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags"
export PERL_PATH=/usr/perl5/bin/perl
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
%{_libdir}/glibmm*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Mar 16 2007 - laca@sun.com
- bump to 2.12.7
* Wed Jan 03 2007 - daymobrew@users.sourceforge.net
- Bump to 2.12.4
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEglibmm
- update permissions
- bump to 2.10.4
* Fri May 12 2006 - damien.carbery@sun.com
- Bump to 2.10.2.
* Fri Mar 10 2006 - damien.carbery@sun.com
- Bump to 2.10.0.
* Thu Nov 17 2005 - laca@sun.com
- create
