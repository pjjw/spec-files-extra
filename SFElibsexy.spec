#
# spec file for package SFElibsexy
#
# includes module(s): libsexy
#

%include Solaris.inc

Name:         SFElibsexy
License:      Other
Group:        System/Libraries
Version:      0.1.11
Summary:      libsexy is a collection of GTK+ widgets that extend the functionality of such standard widget.
Source:       http://releases.chipx86.com/libsexy/libsexy/libsexy-%{version}.tar.gz
URL:          http://www.chipx86.com/wiki/Libsexy
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWiso-codes-devel
Requires: SUNWgnome-base-libs
Requires: SUNWlxml
Requires: SUNWiso-codes

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
%setup -q -n libsexy-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
./configure --prefix=%{_prefix} \
		--libdir=%{_libdir} \
        --disable-gtk-doc
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%dir %attr (0755, root, bin) %dir %{_includedir}/libsexy
%{_includedir}/libsexy/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr (0755, root, bin) %dir %{_datadir}/gtk-doc
%{_datadir}/gtk-doc/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Fri Aug 24 2007 Erwann Chenede <erwann@sun.com>
- bumped to 0.1.11 and removed patch
* Fri Feb 16 2007 - Doug Scott <dougs@truemail.co.th>
- Fixed perm for gtk-doc directory
* Wed Nov 22 2006 - jedy.wang@sun.com
- Initial spec
