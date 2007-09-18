#
# spec file for package SFEcurl
#
# includes module(s): curl
#

%include Solaris.inc

Name:                    SFEcurl
Summary:                 curl - Get a file from FTP or HTTP server.
Version:                 7.17.0
URL:                     http://curl.haxx.se/
Source:                  http://curl.haxx.se/download/curl-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWopenssl-libraries
BuildRequires: SUNWopenssl-include
Requires: SUNWzlib

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%prep
rm -rf %name-%version
%setup -q -n curl-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
# -L/usr/sfw/lib added to CFLAGS to workaround what seems to be a libtool bug
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP -L/usr/sfw/lib"
export RPM_OPT_FLAGS="$CFLAGS"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --includedir=%{_includedir}		\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/curl
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/curl
%{_datadir}/curl/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/curl.1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/curl-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/curl
%{_datadir}/curl/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/curl-config.1
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Tue Sep 18 2007 - nonsea@users.sourceforge.net
- Bump to 7.17.0
* Mon May 28 2007 - Thomas Wagner
- bump to 7.16.2
- --disable-static
* Thu Feb 15 2007 - laca@sun.com
- bump to 7.16.1
* Wed Jan  3 2007 - laca@sun.com
- bump to 7.16.0
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEcurl
- delete -share subpkg
- update attributes to match JDS
- add missing deps
* Sun May 14 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Delete *.la.
* Mon Apr  3 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec

