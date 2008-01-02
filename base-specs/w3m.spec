#
# spec file for package w3m
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#

Name:			w3m
License:		BSD
Group:			Applications/Internet
Version:		0.5.2
Release:	 	4
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		A text-based web browser
Source:			http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
URL:			http://w3m.sourceforge.net/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on
Prereq:                 /sbin/ldconfig

BuildPreReq: openssl-devel >= 0.9.8a, ncurses-devel
BuildPreReq: gdk-pixbuf-devel >= 0.16.0
BuildPreReq: libpng-devel >= 1.2.2, gc-devel

%description
W3m is a pager adapted to World Wide Web. W3m is a text-based WWW
browser as well as a pager.

%prep
%setup -q

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --force
intltoolize --copy --force --automake
aclocal $ACLOCAL_FLAGS  -I .
#autoheader
#automake -a -c -f
#autoconf

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --with-browser=/usr/bin/firefox \
            %gtk_doc_option

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%files
%defattr(-, root, root)
%doc Bonus ChangeLog NEWS README TODO doc doc-jp
%{_sysconfdir}/w3m
%{_bindir}/w3m
%dir %{_libexecdir}/w3m
%{_libexecdir}/w3m/inflate
%dir %{_libexecdir}/w3m/cgi-bin
%{_libexecdir}/w3m/cgi-bin/w3mbookmark
%{_libexecdir}/w3m/cgi-bin/w3mhelperpanel
%{_mandir}/man1/w3m.1*
%{_mandir}/ja/man1/w3m.1*
%{_datadir}/locale/*/*/*
%{_datadir}/w3m/w3mhelp-funcdesc.en.pl
%{_datadir}/w3m/w3mhelp-funcdesc.ja.pl
%{_datadir}/w3m/w3mhelp-funcname.pl
%{_datadir}/w3m/w3mhelp.html

%changelog
* Wed Jan 02 2008 - halton.huo@sun.com
- spilit from SFEw3m.spec
