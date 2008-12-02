#
# spec file for package SFElibupnp
#
# includes module(s): libupnp
#
%include Solaris.inc

%define	src_name libupnp
%define	src_url	http://nchc.dl.sourceforge.net/sourceforge/pupnp

Name:                SFElibupnp
Summary:             Portable C library for UPnP
Version:             1.6.6
Source:              %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		     libupnp-01-solaris.spec
#Patch2:		     libupnp-02-inline.spec
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-DSOLARIS -D_POSIX_PTHREAD_SEMANTICS"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl"

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
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Nov 13 2008 - alfred.peng@sun.com
- Bump to 1.6.6. Remove the inline patch.
  Update the solaris related patch.
* Sun Jul 15 2007 - dougs@truemail.co.th
- Initial spec
