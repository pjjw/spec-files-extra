#
# spec file for package SFElame.spec
#
# includes module(s): lame
#
Name:                    SFElame
Summary:                 lame  - Ain't an MP3 Encoder
Version:                 3.97
Source:                  http://kent.dl.sourceforge.net/sourceforge/lame/lame-%{version}b2.tar.gz
Patch1:                  lame-01-brhist.diff
Patch2:                  lame-02-inline.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms

%prep
%setup -q -n lame-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I%gnu_inc"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="%_ldflags %gnu_lib_path"
export LD_OPTIONS="%gnu_lib_path"

libtoolize --force
autoconf
autoheader
automake -a -c -f
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static
make -j$CPUS LDFLAGS="%{_ldflags}"

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Mar 20 2007 - dougs@truemail.co.th
- Changed to be a base spec
* Mon Jun 12 2006 - laca@sun.com
- rename to SFElame
- change to root:bin to follow other JDS pkgs.
- go back to 02l version of toolame because the beta tarball download site
  is gone.
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
