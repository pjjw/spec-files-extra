#
# spec file for package SFEm17n-contrib
#
# includes module(s): m17n-contrib
#
%include Solaris.inc

%define	src_name m17n-contrib
%define	src_url	http://www.m17n.org/m17n-lib-download

Name:                SFEm17n-contrib
Summary:             m17n Contributed Data
Version:             1.1.3
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEm17n-db-devel
Requires: SFEm17n-db

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-L/usr/sfw/lib -R/usr/sfw/lib"

glib-gettextize --force
aclocal -I m4
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
	    --disable-static			\
	    --enable-shared

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Thu Jul 26 2007 - dougs@truemail.co.th
- Initial spec
