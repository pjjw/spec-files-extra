#
# spec file for package SFEgurlchecker
#
# includes module(s): gurlchecker
#
%include Solaris.inc

%define	src_name gurlchecker
%define	src_url	http://labs.libre-entreprise.org/frs/download.php/547

Name:                SFEgurlchecker
Summary:             Gnome URL Checker
Version:             0.10.1
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     gurlchecker-01-wall.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEdocbook-utils
BuildRequires: SUNWgnutls-devel
Requires: SUNWgnutls
BuildRequires: SUNWlibcroco-devel
Requires: SUNWlibcroco
BuildRequires: SFEclamav-devel
Requires: SFEclamav
BuildRequires: SFEgnet-devel
Requires: SFEgnet

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-D__sun__"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

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
	    --disable-static			\
	    --enable-shared			\
	    --without-tidy			\
	    --enable-compile-warnings=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gurlchecker
%{_datadir}/gtk-doc
%{_mandir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%defattr (-, root, other)
%{_datadir}/locale

%changelog
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
