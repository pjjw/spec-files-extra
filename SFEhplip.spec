#
# spec file for package SFEhplip
#
# includes module(s): hplip
#

%include Solaris.inc

Name:                    SFEhplip
Summary:                 hplip - HP Linux Image and Printing
Group:                   utilities/printing
Version:		 2.8.2
Source:                  %{sf_download}/hplip/hplip-%{version}.tar.gz
Patch1:                  hplip-01-build.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %{name}-root
Requires: SUNWlibusb
Requires: SFEcups
Requires: SUNWsmagt
Requires: SUNWPython
Requires: SFEsane-backends
Requires: SUNWjpg
Requires: SFEpyqt

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n hplip-%{version}
%patch1 -p1

%build
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CFLAGS="%optflags -I/usr/sfw/include"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
export LD="/usr/ccs/bin/ld -L/usr/sfw/lib -R/usr/sfw/lib"
./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}                 \
            --disable-pp-build

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la
# conflict with Solaris
rm $RPM_BUILD_ROOT%{_bindir}/hpijs
#FIXME: move python stuff to vendor-packages
rm $RPM_BUILD_ROOT%{_libdir}/python2.4/site-packages/*.la
rm $RPM_BUILD_ROOT%{_libdir}/sane/lib*.la

# FIXME: add "hpaio" to sane.d/dll.conf some other way
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/sane.d
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/udev

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/cups
%{_libdir}/sane
%{_libdir}/python2.4
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr(0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/hplip
%{_datadir}/cups
%attr(0755, root, lp) %{_datadir}/ppd

%files root
%defattr (-, root, sys)
%{_sysconfdir}/hp

%changelog
* Fri Mar 28 2008 - laca@sun.com
- create
