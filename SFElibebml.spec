#
# spec file for package SFElibebml
#
# includes module(s): libebml
#
%include Solaris.inc

Name:		SFElibebml
License:        LGPL
Summary:        Extensible Binary Meta Language
Group:          System Environment/Libraries
URL:            http://ebml.sourceforge.net/
Vendor:         Moritz Bunkus <moritz@bunkus.org>
Version:	0.7.7
Source:		http://dl.matroska.org/downloads/libebml/libebml-%{version}.tar.bz2
Patch1:		libebml-01-makefile.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libebml-%version
cd make
mkdir solaris
cp linux/Makefile solaris
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

cd make/solaris
make -j$CPUS PREFIX=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
cd make/solaris
make install_headers DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix}
make install_sharedlib DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix}

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

%changelog
* Fri Jul 13 2007 - dougs@truemail.co.th
- Initial version
