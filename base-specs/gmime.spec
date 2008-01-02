#
# spec file for package gmime
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#

Name:			gmime
License:		GPL
Group:			System/Libraries
Version:		2.2.14
Release:	 	4
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Libraries and binaries to parse and index mail messages
Source:			http://download.gnome.org/sources/gmime/2.2/%{name}-%{version}.tar.bz2
URL:			http://spruce.sourceforge.net/gmime/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on
Prereq:                 /sbin/ldconfig

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  glib2-devel >= 1:2.12.1
BuildRequires:  gtk-doc >= 1.0
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel
%if %with_mono
BuildRequires:  dotnet-gtk-sharp2-devel >= 2.9.0
BuildRequires:  mono-csharp >= 1.1.16.1
%endif

%description
This library allows you to manipulate MIME messages.

%package devel
Summary:		Header files to develop libgmime applications
Group:			Development/Libraries
Requires:		%{name} = %{version}
Requires:		glib2-devel >= 1:2.11.4
Requires:               gtk-doc-common
Requires:               zlib-devel

%description devel
Header files develop libgmime applications.


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
#intltoolize --copy --force --automake
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
	    %gtk_doc_option             \
            %mono_option

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
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/libgmime-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgmime-2.0.so.2

%files devel
%defattr(-,root,root)
%doc PORTING
%attr(755,root,root) %{_bindir}/gmime-config
%attr(755,root,root) %{_libdir}/libgmime-2.0.so
%attr(755,root,root) %{_libdir}/gmimeConf.sh
%{_libdir}/pkgconfig/gmime-2.0.pc
%{_includedir}/gmime-2.0
%{_datadir}/gtk-doc/html/gmime

%changelog
* Wed Jan 02 2008 - halton.huo@sun.com
- spilit from SUNWgmime.spec
