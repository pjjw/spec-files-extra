#
# spec file for package SFEkmflcomp
#
# includes module(s): kmflcomp
#
%include Solaris.inc

%define	src_name kmflcomp
%define	src_url	 http://nchc.dl.sourceforge.net/sourceforge/kmfl

Name:                SFEkmflcomp
Summary:             Keyboard Mapping for Linux
Version:             0.9.5
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     kmflcomp-01-wall.diff
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

export CFLAGS="%optflags"
%if %option_with_fox
export CFLAGS="$CFLAGS -I/usr/X11/include"
%endif
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal
automake -a -f
autoconf -f -I autoconf
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --docdir=%{_docdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/doc $RPM_BUILD_ROOT%{_datadir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add support for building on Indiana systems.
* Thu Jul 26 2007 - dougs@truemail.co.th
- Initial spec
