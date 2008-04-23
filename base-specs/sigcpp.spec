#
# spec file for package sigcpp
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#

Name:                    libsigc++
License:                 LGPL
Group:                   System/Libraries
Version:                 2.2.2
Release:                 1
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 Libsigc++ - a library that implements a typesafe callback system for standard C++
URL:                     http://libsigc.sourceforge.net
Source:                  http://ftp.gnome.org/pub/GNOME/sources/libsigc++/2.2/%{name}-%{version}.tar.bz2
#Patch1:                  sigcpp-01-build-fix.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n libsigc++-%version
#%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
perl -pi -e 's/(\s*#define SIGC_TYPEDEF_REDEFINE_ALLOWED.*)/\/\/$1/' \
    sigc++/macros/signal.h.m4
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_cxx_libdir}              \
            --libexecdir=%{_libexecdir}       \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples
cp tests/.libs/test_bind $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_bind
cp tests/.libs/test_bind_ref $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_bind_ref
cp tests/.libs/test_bind_return $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_bind_return
cp tests/.libs/test_compose $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_compose
cp tests/.libs/test_accum_iter $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_accum_iter
cp tests/.libs/test_custom $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_custom
cp tests/.libs/test_disconnect $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_disconnect
cp tests/.libs/test_hide $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_hide
cp tests/.libs/test_slot $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_slot
cp tests/.libs/test_copy_invalid_slot $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_copy_invalid_slot
cp tests/.libs/test_deduce_result_type $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_deduce_result_type
cp tests/.libs/test_disconnect_during_emit $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_disconnect_during_emit
cp tests/.libs/test_exception_catch $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_exception_catch
cp tests/.libs/test_functor_trait $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_functor_trait
cp tests/.libs/test_limit_reference $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_limit_reference
cp tests/.libs/test_mem_fun $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_mem_fun
cp tests/.libs/test_ptr_fun $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_ptr_fun
cp tests/.libs/test_retype $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_retype
cp tests/.libs/test_retype_return $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_retype_return
cp tests/.libs/test_signal $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_signal
cp tests/.libs/test_size $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_size
cp tests/.libs/test_slot_disconnect $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_slot_disconnect
cp tests/.libs/test_trackable $RPM_BUILD_ROOT%{_datadir}/doc/libsigc-2.0/examples/test_trackable

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.2.2.
* Fri Feb 29 2008 - elaine.xiong@sun.com
- Bump to 2.2.1 that resolves build failure of 2.2.0 with CC.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.2.0.
* Fri Feb 22 2008 - elaine.xiong@sun.com
- Include tests binaries into dev package.
* Tue Feb 12 2008 - ghee.teo@sun.com
- Clean up %files section
* Fri Feb 01 2008 - elaine.xiong@sun.com
- create. split from SFEsigcpp.spec
