#
# spec file for package SFEclutter
#
# includes module(s): clutter
#
%include Solaris.inc

Name:                    SFEclutter
Summary:                 clutter - a library for creating fast, visually rich and animated graphical user interfaces.
Version:                 0.4.0
URL:                     http://www.clutter-project.org/
Source:                  http://www.clutter-project.org/sources/clutter/0.4/clutter-%{version}.tar.bz2
Patch1:                  clutter-01-build.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel


%prep
%setup -q -n clutter-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Aug  9 2007 - laca@sun.com
- bump to 0.4.0
* Thu Jul 19 2007 - laca@sun.com
- create
