#
# spec file for package giflib
#
# includes module(s): giflib
#

%define src_ver 4.1.4
%define src_name giflib
#%define src_url http://%{sf_mirror}/libungif
%define src_url http://%{sf_mirror}/giflib

Name:		giflib
Summary:	GIF-manipulation library
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		giflib-01-configure.diff
Patch2:		giflib-02-giftext-segfault.diff
Patch3:		giflib-03-wall.diff
Patch4:		giflib-04-u_int.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize -f -c
aclocal
autoconf -f
autoheader
automake -a -f

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
rm -f $RPM_BUILD_ROOT%{_libdir}/giflib/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Mar 21 2008 - Thomas Wagner
- adjust download URL
* Thu Sep  6 2007 - dougs@truemail.co.th
- Initial base spec file
