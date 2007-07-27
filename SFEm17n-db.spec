#
# spec file for package SFEm17n-db
#
# includes module(s): m17n-db
#
%include Solaris.inc

%define	src_name m17n-db
%define	src_url	http://www.m17n.org/m17n-lib-download
%define glibc_ver 2.6
%define glibc_name glibc
%define	glibc_url http://ftp.gnu.org/gnu/glibc

Name:                SFEm17n-db
Summary:             m17n database
Version:             1.4.0
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Source1:             %{glibc_url}/%{glibc_name}-%{glibc_ver}.tar.bz2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -c -b 1 -q -n %{name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd %{src_name}-%{version}
set

charmaps=$RPM_BUILD_DIR/%{name}-%{version}/%{glibc_name}-%{glibc_ver}/localedata/charmaps/
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

glib-gettextize --force
aclocal
libtoolize --copy --force 
automake -a -f
autoconf -f 
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --with-charmaps=$charmaps		\
	    --disable-static			\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/m17n

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Jul 26 2007 - dougs@truemail.co.th
- Initial spec
