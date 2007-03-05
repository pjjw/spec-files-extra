#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFElighttpd
Summary:             A light httpd
Version:             1.4.13
Source:              http://www.lighttpd.net/download/lighttpd-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWpcre-devel
Requires: SUNWpcre
Requires: SUNWopenssl-commands
BuildRequires: SUNWopenssl-commands
# The line above pretty much guarantees that the other SUNWopenssl*
# will be installed as well

%prep
%setup -q -n lighttpd-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix}  \
            --with-openssl="/usr/sfw" \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/mod_*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/spawn-fcgi
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/lighttpd
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/mod*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/lighttpd.1  
%{_mandir}/man1/spawn-fcgi.1

%changelog
* 
* Sun Mar 04 2007 - Eric Boutilier
- Initial spec
