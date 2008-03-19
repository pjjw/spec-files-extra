#
# spec file for package SFEjabberd
#
# includes module(s): jabberd
#
%include Solaris.inc

%define	src_name jabberd
%define	src_url	http://ftp.xiaoka.com/jabberd2/releases

Name:                SFEjabberd
Summary:             Jabber - XMPP Server
Version:             2.1.11
Source:              %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		     jabberd-01-string-conversion.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEexpat
BuildRequires: SFEgsslib-devel
Requires: SFEgsslib
BuildRequires: SUNWsqlite3
Requires: SUNWsqlite3
BuildRequires: SUNWpostgr-82-devel
Requires: SUNWpostgr-82-libs
Requires: SFEbdb
Requires: SUNWmysqlu
Requires: SUNWmysqlr

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I/usr/gnu/include -I/usr/postgres/8.2/include -I/usr/sfw/include/mysql -I/usr/sfw/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-L/usr/gnu/lib -L/usr/postgres/8.2/lib -L/usr/sfw/lib -R/usr/postgres/8.2/lib:/usr/gnu/lib:/usr/sfw/lib"

glib-gettextize --force
aclocal
libtoolize --copy --force 
automake -a -f
autoconf -f 
./configure --prefix=%{_prefix}				\
            --bindir=%{_bindir}				\
            --libdir=%{_libdir}				\
            --sysconfdir=%{_sysconfdir}/jabberd		\
            --includedir=%{_includedir} 		\
            --mandir=%{_mandir}				\
	    --infodir=%{_infodir}			\
	    --disable-static				\
	    --enable-shared				\
	    --enable-mysql				\
	    --enable-pgsql				\
	    --enable-sqlite				\
	    --enable-db

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Thu Jul 26 2007 - dougs@truemail.co.th
- Initial spec
