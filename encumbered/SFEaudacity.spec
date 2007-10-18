#
# spec file for package SFEaudacity
#
# includes module(s): audacity
#
%include Solaris.inc

%define	src_name audacity
%define	src_url	http://nchc.dl.sourceforge.net/sourceforge/audacity

Name:                SFEaudacity
Summary:             manipulate digital audio waveforms
Version:             1.3.3
Source:              %{src_url}/%{src_name}-src-%{version}.tar.gz
Patch1:		     audacity-01-solaris.diff
Patch2:		     audacity-02-portaudio.diff
Patch3:		     audacity-03-alloca.diff
Patch4:		     audacity-04-twolame.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibmad-devel
Requires: SFElibmad
BuildRequires: SFElibsamplerate-devel
Requires: SFElibsamplerate
BuildRequires: SFElibid3tag-gnu-devel
Requires: SFElibid3tag-gnu-devel
BuildRequires: SFEportaudio-devel
Requires: SFEportaudio
BuildRequires: SFEwxwidgets-gnu-devel
Requires: SFEwxwidgets-gnu
BuildRequires: SFEgcc
BuildRequires: SFEgettext

%prep
%setup -q -n %{src_name}-src-%{version}-beta
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%if %debug_build
export CFLAGS="-g"
dbgopt=-enable-debug --enable-debug-output
%else
export CFLAGS="-O4"
dbgopt=-disable-debug
%endif

export CPPFLAGS="-I/usr/gnu/include -I/usr/X11/include -I/usr/sfw/include"
export PATH=/usr/gnu/bin:$PATH
export LDFLAGS="-L/usr/gnu/lib -L/usr/X11/lib -R/usr/gnu/lib -R/usr/X11/lib -R/usr/sfw/lib"
export CC=gcc
export CXX=g++
CFLAGS="$CFLAGS -fPIC -DPIC -fno-omit-frame-pointer"
CXXFLAGS="$CFLAGS -fPIC -DPIC -fno-omit-frame-pointer"

libtoolize -f -c
aclocal
autoconf -f
autoheader

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --datadir=%{_datadir}       \
            --libdir=%{_libdir}         \
            --mandir=%{_mandir}         \
            $dbgopt

# /usr/gnu/bin/gcc is using gnu ld....
perl -pi -e 's/-M ...wl./--version-script=/' lib-src/portaudio-v19/libtool
perl -pi -e 's/-Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect//' src/Makefile
perl -pi -e 's/-Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect//' tests/Makefile

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/audacity
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (-, root, root) %{_datadir}/mime
%attr (-, root, root) %{_datadir}/mime/*

%changelog
* Sat Sep 22 2007 - dougs@truemail.co.th
- Initial spec
