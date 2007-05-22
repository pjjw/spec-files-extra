#
# spec file for package SFEid3lib
#
# includes module(s): id3lib
#
#
%include Solaris.inc

Name:                    SFEid3lib
Summary:                 id3lib  - a software library for manipulating ID3v1/v1.1 and ID3v2 tags
Version:                 3.8.3
Source:                  http://nchc.dl.sourceforge.net/sourceforge/id3lib/id3lib-%{version}.tar.gz
Patch1:                  id3lib-01-wall.diff
Patch2:                  id3lib-02-uchar.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
Requires: SUNWlibC
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n id3lib-%version
%patch1  -p1
%patch2  -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
%ifarch sparc
export CFLAGS="-xO5 -xlibmil"
export CXXFLAGS="-norunpath -xO5 -xlibmil -xlibmopt -features=tmplife"
%else
export CFLAGS="-xO3 -xlibmil"
export CXXFLAGS="-norunpath -xO3 -xlibmil -xlibmopt -features=tmplife"
%endif

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-fpm=%{fp_arch}          \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFEid3lib
- changed to root:bin to follow other JDS pkgs.
- added dependencies
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
