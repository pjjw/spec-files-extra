#
# spec file for package libquicktime
#
# includes module(s): libquicktime
#

%define src_ver 1.0.0
%define src_name libquicktime
%define src_url http://downloads.sourceforge.net/%{src_name}

Name:		libquicktime
Summary:	Quicktime library
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libquicktime-01-configure.diff
Patch2:		libquicktime-02-gtk.diff
Patch3:		libquicktime-03-rtjpeg.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags -I/usr/X11/include"
export LDFLAGS="%_ldflags"
export AVCODEC_CFLAGS="%optflags"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export CFLAGS="$CFLAGS -m64"
        export CXXFLAGS="$CXXFLAGS -m64"
        export LDFLAGS="-Wl,-64 -L%{_libdir} -L/usr/X11/lib/%{_arch64} -R%{_libdir}:/usr/X11/lib/%{_arch64} $LDFLAGS"
else
        export LDFLAGS="-L%{_libdir} -L/usr/X11/lib -R%{_libdir}:/usr/X11/lib $LDFLAGS"
fi

bash autogen.sh

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --enable-shared		\
	    --disable-static
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/libquicktime/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Fixed links
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Add a patch to fix a compile failure with Sun Studio 11
* Tue Sep  4 2007 - dougs@truemail.co.th
- Initial base spec file
