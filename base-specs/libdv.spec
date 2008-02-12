#
# spec file for package libdv
#
# includes module(s): libdv
#

%define src_ver 1.0.0
%define src_name libdv
%define src_url http://downloads.sourceforge.net/libdv

Name:		libdv
Summary:	The Quasar DV codec
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libdv-01-solaris.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags"
export LDFLAGS="%arch_ldadd %ldadd ${EXTRA_LDFLAGS}"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export CFLAGS="$CFLAGS -m64"
        export LDFLAGS="-Wl,-64 -L%{_libdir} -R%{_libdir} $LDFLAGS"
	gtkopt=--disable-gtk
	asmopt=--disable-asm
fi

libtoolize -f -c
aclocal
autoheader
autoconf -f
automake -a -f

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --enable-shared		\
	    --disable-static		\
	    $gtkopt $asmopt

perl -pi -e 's,-shared,-Wl,-G' libtool
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/libdv/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Fixed links
* Tue Nov 20 2007 - daymobrew@users.sourceforge.net
- Change LDFLAGS to work for gcc.
* Thu Aug 30 2007 - dougs@truemail.co.th
- Initial base spec file
