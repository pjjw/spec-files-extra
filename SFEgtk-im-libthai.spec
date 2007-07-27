#
# spec file for package SFEgtk-im-libthai
#
# includes module(s): gtk-im-libthai
#
%include Solaris.inc

%define	src_name gtk-im-libthai
%define	src_url	ftp://linux.thai.net/pub/thailinux/software/libthai

Name:                SFEgtk-im-libthai
Summary:             Thai language gtk im module
Version:             0.1.4
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibthai-devel
Requires: SFElibthai
BuildRequires: SFElibdatrie-devel
Requires: SFElibdatrie

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal
automake -a -f
autoconf -f -I autoconf
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/immodules/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules

%postun
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules

%files
%defattr (-, root, bin)
%{_libdir}

%changelog
* Thu Jul 26 2007 - dougs@truemail.co.th
- Initial spec
