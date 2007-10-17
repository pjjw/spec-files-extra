#
# spec file for package SFElibstroke
#
# includes module(s): libstroke
#
%include Solaris.inc

%define	src_name libstroke
%define	src_url	http://www.etla.net/%{src_name}

Name:		SFElibstroke
Summary:	A stroke translation library
Version:	0.5.1
License:	GPL
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libstroke-01-am15.diff
Patch2:		libstroke-02-am18.diff
Patch3:		libstroke-03-link.diff
Patch4:		libstroke-04-no-gtk1.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%description
LibStroke is a stroke translation library. Strokes are motions of the
mouse that can be interpreted by a program as a command. Strokes are
used extensively in CAD programs.

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PKG_CONFIG_PATH=/usr/sfw/lib/pkgconfig
export CPPFLAGS="-I/usr/sfw/include -I/usr/X11/lib"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export LD_LIBRARY_PATH="-L/usr/sfw/lib -R/usr/sfw/lib -L/usr/X11/lib -RL/usr/X11/lib"

libtoolize --copy --force
aclocal -I /usr/sfw/share/aclocal
autoconf -f
automake -a -c -f
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared		\
	    --disable-gtktest

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Wed Oct 17 2007 - laca@sun.com
- add patch no-gtk1.diff that disables gtk-1.x support
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
