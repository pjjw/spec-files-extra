#
# spec file for package SFElibglademm
#
# includes module(s): libglademm
#
%include Solaris.inc

Name:                    SFElibglademm
Summary:                 libglademm - C++ Wrapper for the Gtk+ Library
Version:                 2.6.3
URL:                     http://www.gtkmm.org/
Source:                  http://ftp.acc.umu.se/pub/GNOME/sources/libglademm/2.6/libglademm-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEglibmm
Requires: SFEcairomm
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
Requires: SUNWmlib
Requires: SFEsigcpp
Requires: SUNWlibC
Requires: SFEgtkmm
BuildRequires: SFEsigcpp-devel
BuildRequires: SFEglibmm-devel
BuildRequires: SFEcairomm-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFEgtkmm-devel

%package devel
Summary:                 libglademm - C++ Wrapper for the Gtk+ Library - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SFEglibmm-devel
Requires: SFEsigcpp-devel


%prep
%setup -q -n libglademm-%version

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
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} --disable-python
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT%{_datadir}/devhelp
#mv $RPM_BUILD_ROOT%{_bindir}/demo $RPM_BUILD_ROOT%{_bindir}/libglademm-demo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
#%dir %attr (0755, root, bin) %{_bindir}
#%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Jun 05 2007 Thomas Wagner
- needed by pulseaudio frontends
- initial version from the museeum of spec-files (copy of SFEgtkmm.spec)
