#
# spec file for package liba52
#
# includes module(s): liba52
#

Name:                    liba52
Summary:                 liba52  - a free library for decoding ATSC A/52 streams
Version:                 0.7.4
Source:                  http://liba52.sourceforge.net/files/a52dec-%{version}.tar.gz
Patch1:			 liba52-01-pic.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n a52dec-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

libtoolize -f -c
aclocal
autoconf -f
autoheader -f
automake -a -f
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --enable-shared		\
	    --disable-static		\
	    --with-pic

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%changelog
* Wed Aug 15 2007 - dougs@truemail.co.th
- Convert to base spec
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFEliba52
- changed to root:bin to follow other JDS pkgs.
- added dependencies
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
