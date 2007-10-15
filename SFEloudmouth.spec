#
# spec file for package SFEloudmouth
#
# includes module(s): loudmouth
#
%include Solaris.inc

Name:                    SFEloudmouth
Summary:                 Loudmouth - C library for the Jabber protocol
Version:                 1.2.2
Source:                  http://ftp.imendio.com/pub/imendio/loudmouth/src/loudmouth-%{version}.tar.gz
URL:                     http://www.loudmouth-project.org/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: CBEbison
BuildRequires: SUNWPython
Requires: SUNWgnome-libs

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n loudmouth-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
glib-gettextize -f
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
%{_libdir}/lib*so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc/html/loudmouth

%changelog
* Sun Oct 14 2007 - laca@sun.com
- bump to 1.2.2
* Wed Jul  5 2006 - laca@sun.com
- rename to SFEloudmouth
- add -devel subpkg
- update file attributes
- delete unnecessary env variables
* Thu Jun  1 2006 - glynn.foster@sun.com
- Initial version
