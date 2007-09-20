#
# spec file for package SFEgtkmm
#
# includes module(s): gtkmm
#
%include Solaris.inc

Name:                    SFEgtkmm
Summary:                 gtkmm - C++ Wrapper for the Gtk+ Library
Version:                 2.10.11
URL:                     http://www.gtkmm.org/
Source:                  http://ftp.acc.umu.se/pub/GNOME/sources/gtkmm/2.10/gtkmm-%{version}.tar.bz2
Patch1:                  gtkmm-01-tooltips.diff
Patch2:                  gtkmm-02-getc_unlocked.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEglibmm
Requires: SFEcairomm
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
Requires: SFEsigcpp
Requires: SUNWlibC
BuildRequires: SFEsigcpp-devel
BuildRequires: SFEglibmm-devel
BuildRequires: SFEcairomm-devel
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:                 gtkmm - C++ Wrapper for the Gtk+ Library - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SFEglibmm-devel
Requires: SFEsigcpp-devel


%prep
%setup -q -n gtkmm-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D__EXTENSIONS__"

autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT%{_datadir}/devhelp
mv $RPM_BUILD_ROOT%{_bindir}/demo $RPM_BUILD_ROOT%{_bindir}/gtkmm-demo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/gtkmm*
%{_libdir}/gdkmm*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Sep 19 2007 - trisk@acm.jhu.edu
- Add patch1, patch2, change CFLAGS
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 2.10.11
* Tue Apr 17 2007 - daymobrew@users.sourceforge.net
- bump to 2.10.9.
* Fri Mar 16 2007 - laca@sun.com
- bump to 2.10.8
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEgtkmm
- update permissions
* Thu Nov 17 2005 - laca@sun.com
- create
