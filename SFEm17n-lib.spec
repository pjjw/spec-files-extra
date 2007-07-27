#
# spec file for package SFEm17n-lib
#
# includes module(s): m17n-lib
#
%include Solaris.inc

%define	src_name m17n-lib
%define	src_url	http://www.m17n.org/m17n-lib-download

Name:                SFEm17n-lib
Summary:             m17n library
Version:             1.4.0
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     m17n-lib-01-intl.diff
Patch2:		     m17n-lib-02-alloca.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEm17n-db-devel
Requires: SFEm17n-db
BuildRequires: SFEwordcut-devel
Requires: SFEwordcut
BuildRequires: SFEgd-devel
Requires: SFEgd
BuildRequires: SFElibanthy-devel
Requires: SFElibanthy
BuildRequires: SFElibfribidi-devel
Requires: SFElibfribidi
BuildRequires: SFElibthai-devel
Requires: SFElibthai
BuildRequires: SFElibotf-devel
Requires: SFElibotf

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch2 -p1

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
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -rf $RPM_BUILD_ROOT%{_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Jul 26 2007 - dougs@truemail.co.th
- Initial spec
