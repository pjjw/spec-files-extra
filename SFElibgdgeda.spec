#
# spec file for package SFElibgdgeda
#
# includes module(s): libgdgeda
#
%include Solaris.inc

%define	src_ver 2.0.15
%define	src_name libgdgeda
%define	src_url	ftp://ftp.geda.seul.org/pub/geda/devel/support

Name:		SFElibgdgeda
Summary:	Hack of libgd library for gEDA project
Version:	%{src_ver}
License:	GPL
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Libgdgeda is a hack on libgd, which is a graphics library. It allows
your code to quickly draw images complete with lines, arcs, text,
multiple colors, cut and paste from other images, and flood fills, and
write out the result as a .PNG file.

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_prefix}
%include default-depend.inc
Requires: %name

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
autoconf -f
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
install -d $RPM_BUILD_ROOT%{_datadir}/gEDA/scheme

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gEDA

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
