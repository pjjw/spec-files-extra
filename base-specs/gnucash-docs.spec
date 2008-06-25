#
# spec file for package gnucash-docs
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#


Name:           gnucash-docs
Summary:        This is the documentation module for GnuCash
License:        GNU Free Documentation License
Group:          Applications/Finance
Version:        2.2.0
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.gnucash.org/
Source:         http://www.gnucash.org/pub/gnucash/sources/stable/%{name}-%{version}.tar.gz
BuildRoot:      %{tmpdir}/%{name}-%{version}-root

Requires:       gnucash >= 1.8.0, scrollkeeper >= 0.3.4
BuildPrereq:    docbook-style-xsl


%description
GnuCash is a personal finance manager. A check-book like
register GUI allows you to enter and track bank accounts,
stocks, income and even currency trades. The interface is
designed to be simple and easy to use, but is backed with
double-entry accounting principles to ensure balanced books.
This is the documentation module for GnuCash.

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

aclocal $ACLOCAL_FLAGS -I .
libtoolize --force
automake -a -f -c --gnu
autoconf

CFLAGS="$RPM_OPT_FLAGS"
./configure  --prefix=%{_prefix}

make -j $CPUS


%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%clean
rm -rf $RPM_BUILD_ROOT

%post
if which scrollkeeper-update>/dev/null 2>&1; then scrollkeeper-update -o %{_datadir}/omf/gnucash-docs; fi

%postun
if which scrollkeeper-update>/dev/null 2>&1; then scrollkeeper-update; fi


%files
%defattr(-,root,root)
%{_datadir}/gnome/help/gnucash
%{_datadir}/omf/gnucash-docs
%doc AUTHORS COPYING-DOCS ChangeLog NEWS README HACKING

%changelog
* Wed Jun 25 2008 - nonsea@users.sourceforge.net
- Initial version
