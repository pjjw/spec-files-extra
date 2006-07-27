#
# spec file for package SFElame.spec
#
# includes module(s): lame, toolame
#
%include Solaris.inc

Name:                    SFElame
Summary:                 lame  - Ain't an MP3 Encoder
Version:                 3.97
Source:                  http://kent.dl.sourceforge.net/sourceforge/lame/lame-%{version}b2.tar.gz
%define toolame_version   02l
Source2:                  http://kent.dl.sourceforge.net/sourceforge/toolame/toolame-%{toolame_version}.tgz
Patch1:                   lame-01-brhist.diff
Patch2:                   lame-02-inline.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n lame-%version
%patch1 -p1
%patch2 -p1
cd ..
gtar fxvz %SOURCE2
cd toolame-%{toolame_version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

libtoolize --force
autoconf
autoheader
automake -a -c -f
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-fpm=%{fp_arch}          \
            --enable-shared		     \
	    --disable-static
make -j$CPUS LDFLAGS="%{_ldflags}"

cd ../toolame-%{toolame_version}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd ../toolame-%{toolame_version}
#make install DESTDIR=$RPM_BUILD_ROOT
install -m 755 toolame $RPM_BUILD_ROOT%{_bindir}/toolame
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/doc/*

%changelog
* Mon Jun 12 2006 - laca@sun.com
- rename to SFElame
- change to root:bin to follow other JDS pkgs.
- go back to 02l version of toolame because the beta tarball download site
  is gone.
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
