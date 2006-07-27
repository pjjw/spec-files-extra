#
# spec file for package SFElibsndfile
#
# includes module(s): libsndfile
#
%include Solaris.inc

Name:                    SFElibsndfile
Summary:                 libsndfile  - a library of C routines for reading and writing files containing sampled audio data
Version:                 1.0.16
Source:                  http://www.mega-nerd.com/libsndfile/libsndfile-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWflac
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libsndfile-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%{_datadir}/octave

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Mon Jun 12 2006 - laca@sun.com
- rename to SFElibsndfile
- change to root:bin to follow other JDS pkgs.
- get rid of -share pkg
- move stuff around between base and -devel
- add missing deps
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
