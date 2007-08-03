#
# spec file for package SFEfoomatic-db-engine
#
# includes module(s): foomatic-db-engine
#
%include Solaris.inc

%define	src_ver 3.0.2
%define	src_name foomatic-db-engine
%define	src_url	http://www.linuxprinting.org/download/foomatic

Name:		SFEfoomatic-db-engine
Summary:	Foomatic database Engine
Version:	%{src_ver}
License:	GPL
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		foomatic-db-engine-01-perl.diff
Patch2:		foomatic-db-engine-02-null.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Foomatic is a system for using free software printer drivers with
common spoolers on Unix. It supports LPD, PDQ, CUPS, the VA Linux LPD,
LPRng, PPR, and direct spooler-less printing and any free software
driver for which execution data has been entered in the database.

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch2 -p1

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PATH=$PATH:/usr/sfw/bin
export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="-g %optflags"
export CFLAGS="-g"
export LDFLAGS="%_ldflags -lX11"
export LD_OPTIONS="-L/usr/sfw/lib -R/usr/sfw/lib"
export FILEUTIL=/usr/gnu/bin

bash make_configure
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared			\
	    --enable-debug
make

%install
rm -rf $RPM_BUILD_ROOT
( cd lib && /usr/bin/perl Makefile.PL verbose INSTALLDIRS=vendor )
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_sbindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/foomatic
%{_mandir}
%{_prefix}/perl5

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
