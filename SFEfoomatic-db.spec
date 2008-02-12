#
# spec file for package SFEfoomatic-db
#
# includes module(s): foomatic-db
#
%include Solaris.inc

%define	src_ver 3.0
%define	src_name foomatic-db
%define	src_url	http://www.linuxprinting.org/download/foomatic

Name:		SFEfoomatic-db
Summary:	Foomatic database
Version:	current
License:	GPL
Source:		%{src_url}/%{src_name}-%{src_ver}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PATH=$PATH:/usr/sfw/bin
export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lX11"
export LD_OPTIONS="-L/usr/sfw/lib -R/usr/sfw/lib"
export FILEUTIL=/usr/gnu/bin

aclocal
autoconf -f
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared			\
	    --disable-debug
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/foomatic
%{_datadir}/cups

%changelog
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
