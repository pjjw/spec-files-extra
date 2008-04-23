#
# spec file for package gtkmm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
Name:         gtkmm
License:      LGPL
Group:        System/Libraries
Version:      2.12.4
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      gtkmm - C++ Interfaces for GTK+ and GNOME
Source:       http://download.gnome.org/sources/gtkmm/2.12/gtkmm-%{version}.tar.bz2

#date:2008-02-14 owner:bewitche type:feature  
Patch1:       gtkmm-01-ignore-defs.diff
# date:2008-02-14 owner:bewitche type:bug bugzilla:516600
Patch2:	      gtkmm-02-demo.diff  
# date:2008-02-14 owner:bewitche type:bug bugzilla:516602
Patch3:       gtkmm-03-demo-installation.diff
# date:2008-02-18 owner:dcarbery type:bug bugzilla:423990
Patch4:       glibmm-01-m4-macro.diff
URL:          http://www.gtkmm.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n gtkmm-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# background.jpg is required by gtkmm-demo, but not in the right directory
# we simply copy the file into the proper directory
cp ./demos/background.jpg ./demos/gtk-demo

automake --add-missing
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_cxx_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
mv $RPM_BUILD_ROOT%{_bindir}/demo $RPM_BUILD_ROOT%{_bindir}/gtkmm-demo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*


%changelog
* Fri Fe 22 2008 - damien.carbery@sun.com
- Add glibmm-02-m4-macro to fix #423990. Use glibmm patch as issue is identical.
* Thu Feb 14 2008 - chris.wang@sun.com
- Add patches gtkmm-02-demo, gtkmm-03-demo-installation to deliver gtkmm-demo
  on /usr/demo/jds/bin and resource files on /usr/share/gtkmm-2.4/demo
* Thu Feb 14 2008 - chris.wang@sun.com
- Add patch gtkmm-01-ignore-defs to remove the build of defs files since they
  are delivered with tarball and libglibmm_generate_extra_defs.so is not 
  delivered. We have raise this issue to module owner, and will remove the 
  patch if the module owner agree to remove .def file from tarball
* Tue Jan 29 2008 - chris.wang@sun.com
- create
