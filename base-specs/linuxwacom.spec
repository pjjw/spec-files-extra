#
# spec file for package linuxwacom
#
# includes module(s): linuxwacom
#

%define src_name         linuxwacom	

Summary:                 Wacom input device driver for X.org
Version:                 0.8.2
Source:                  %{sf_download}/linuxwacom/%{src_name}-%{version}.tar.bz2
URL:                     http://linuxwacom.sourceforge.net/
Patch1:                  linuxwacom-01-no-usb.diff
Patch2:                  linuxwacom-02-sunpro.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov:             on

%prep
%setup -q -n%{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    XMODULEDIR="%{_prefix}/X11/lib/modules/input/%{_arch64}"
else
    XMODULEDIR="%{_prefix}/X11/lib/modules/input"
fi

export CPPFLAGS="-I%{xorg_inc}"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags %{xorg_lib_path}"

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
bash ./configure	\
    --prefix=%{_prefix}/X11 \
    --mandir=%{_prefix}/X11/share/man	\
    --with-x	\
    --with-xmoduledir=$XMODULEDIR

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_prefix}/X11/lib/*.a
rm -f $RPM_BUILD_ROOT%{_prefix}/X11/lib/*.la


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Dec 16 2008 - trisk@acm.jhu.edu
- Initial spec
