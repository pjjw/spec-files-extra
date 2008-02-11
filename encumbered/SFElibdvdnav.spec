#
# spec file for package SFElibdvdnav
#
# includes module(s): libdvdnav
#
%include Solaris.inc

Name:                    SFElibdvdnav
Summary:                 libdvdnav  - DVD navigation library
Version:                 0.1.10
Source:                  %{sf_download}/dvd/libdvdnav-%{version}.tar.gz
Patch1:                  libdvdnav-01-Wall.diff
SUNW_BaseDir:            %{_basedir}
buildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n libdvdnav-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

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
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dvdnav-config
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Sun Jan  7 2007 - laca@sun.com
- create
