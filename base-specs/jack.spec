#
# spec file for package jack
#
# includes module(s): jack
#

%define src_ver 0.103.0
%define src_name jack-audio-connection-kit
%define src_url http://nchc.dl.sourceforge.net/sourceforge/jackit

Name:		jack
Summary:	Jack Audio Connection Kit
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		jack-01-svn1051.diff
Patch2:		jack-02-solaris.diff
Patch3:		jack-03-timersub.diff
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

%if %debug_build
dbgflag=--disable-debug
%else
dbgflag=--disable-debug
%endif

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

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
	    --with-default-tmpdir="/tmp"\
            --enable-shared		\
	    --disable-static

make # -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/jack/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Aug 28 2007 - dougs@truemail.co.th
- Added debug option
- Patched with latest svn release
- Solaris patch now contains many fixes and code for real time with RBAC
* Mon Aug 13 2007 - dougs@truemail.co.th
- Initial base spec file
