#
# spec file for package SFEshishi
#
# includes module(s): shishi
#
%include Solaris.inc

%define	src_name shishi
%define	src_url	http://josefsson.org/shishi/releases

Name:		SFEshishi
Summary:        Shishi - an implementation of RFC 1510(bis) (Kerberos V5 authentication)
Version:        0.0.32
License:	GPL v3+
Source:         %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		shishi-01-min.diff
Patch2:		shishi-02-include_next.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEfix-info-dir
BuildRequires: SFElibidn-devel
Requires: SFElibidn
BuildRequires: SFElibtasn1-devel
Requires: SFElibtasn1
BuildRequires: SUNWgnutls-devel
Requires: SUNWgnutls

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
rm m4/gettext.m4

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

aclocal -I m4 -I gl/m4
libtoolize --copy --force 
automake -a -f
autoconf -f 
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --sbindir=%{_sbindir}		\
            --libdir=%{_libdir}			\
            --sysconfdir=%{_sysconfdir}		\
	    --localstatedir=%{_localstatedir}	\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-rpath			\
	    --disable-static			\
	    --enable-shared
make -j$CPUS
%patch2 -p1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/security/pam_*.*a
(
   cd $RPM_BUILD_ROOT%{_libdir}/security
   mv pam_shishi.so pam_shishi.so.1
   ln -s pam_shishi.so.1 pam_shishi.so
)

rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
  echo '/usr/sbin/fix-info-dir' | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
  echo '/usr/sbin/fix-info-dir' | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%{_bindir}
%{_sbindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/security
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%defattr (-, root, sys)
%{_sysconfdir}
%{_localstatedir}

%changelog
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
