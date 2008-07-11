#
# spec file for package SFElibcddb
#
# includes module(s): libcddb
#
%include Solaris.inc

%define	src_name libcddb
%define	src_url	http://jaist.dl.sourceforge.net/sourceforge/%{src_name}

Name:                SFElibcddb
Summary:             C library to access data on a CDDB server
Version:             1.3.0
Source:              %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:            SFElibiconv
BuildRequires:       SFElibiconv-devel
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I /usr/gnu/share/aclocal"

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -f
autoconf -f
./configure --prefix=%{_prefix}           \
            --bindir=%{_bindir}           \
            --libdir=%{_libdir}           \
            --includedir=%{_includedir}   \
            --mandir=%{_mandir}           \
	         --infodir=%{_infodir}         \
	         --disable-static              \
	         --enable-shared               \
            --without-cdio

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

#Move cddb_query example to demo directoty
install -d $RPM_BUILD_ROOT%{_prefix}/demo/libcddb/bin
mv $RPM_BUILD_ROOT%{_bindir}/cddb_query \
                  $RPM_BUILD_ROOT%{_prefix}/demo/libcddb/bin/cddb_query

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_bindir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_prefix}/demo/libcddb/bin/cddb_query

%changelog
* Fri Jul 11 2008 - andras.barna@gmail.com
- Add ACLOCAL_FLAGS, SFElibiconv dep
* Mon Feb 04 2008 - Michal dot Pryc [(at] Sun . Com
- cddb_query is an example utlility. Moved to devel package, now it is installed
  under /usr/demo/libcddb/bin/cddb_query
- build without cdio support. Affects only cddb_query example utility.
* Sat Jul 14 2007 - dougs@truemail.co.th
- Initial spec
