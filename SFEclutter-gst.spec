#
# spec file for package SFEclutter-gst
#
# includes module(s): clutter-gst
#
%include Solaris.inc

Name:                    SFEclutter-gst
Summary:                 clutter-gst - gstreamer integration library for clutter
Version:                 0.4.0
URL:                     http://www.clutter-project.org/
Source:                  http://www.clutter-project.org/sources/clutter-gst/0.4/clutter-gst-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SFEclutter
Requires: SUNWgnome-media
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SFEclutter-devel
Requires: SUNWgnome-media-devel


%prep
%setup -q -n clutter-gst-%version

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
- delete upstream patch
* Thu Jul 19 2007 - laca@sun.com
- create
