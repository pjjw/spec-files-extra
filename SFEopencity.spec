#
# spec file for package SFEopencity.spec
#
# includes module(s): opencity
#
%include Solaris.inc

Name:                    SFEopencity
Summary:                 opencity - OpenCity Game
Version:                 0.0.4stable
Source:                  http://nchc.dl.sourceforge.net/sourceforge/opencity/opencity-%{version}.tar.bz2
Patch1:			 opencity-01-makefile.diff
Patch2:			 opencity-02-homedir.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEsdl-ttf-devel
Requires: SFEsdl-ttf
BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-mixer
BuildRequires: SFEsdl-net-devel
Requires: SFEsdl-net

%prep
%setup -q -n opencity-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

export CXX=/usr/sfw/bin/g++
export CXXFLAGS="-O3 -Xlinker -i -fno-omit-frame-pointer -fpic -Dpic"
libtoolize --copy
aclocal
automake
autoconf --force
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
make install DESTDIR=$RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/pixmaps
%{_datadir}/opencity
%{_datadir}/applications

%changelog
* Sun Apr 22 2007 - dougs@truemail.co.th
- Initial version
