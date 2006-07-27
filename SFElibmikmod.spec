#
# spec file for package SFElibmikmod
#
# includes module(s): libmikmod
#
%include Solaris.inc

Name:                    SFElibmikmod
Summary:                 libmikmod  - a portable sound library for Unix and other systems.
Version:                 3.2.0
%define tarball_version 3.2.0-beta2
Source:                  http://mikmod.raphnet.net/files/libmikmod-%{tarball_version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libmikmod-%tarball_version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/usr/info
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/libmikmod-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibmikmod
- changed to root:bin to follow other JDS pkgs.
- add missing dep
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
