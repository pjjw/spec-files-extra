#
# spec file for package SFEsdl
#
# includes module(s): SDL
#
%include Solaris.inc

Name:                    SFEsdl
Summary:                 Simple DirectMedia - multimedia library
Version:                 1.2.11
Source:                  http://www.libsdl.org/release/SDL-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms
Requires: SUNWxwrtl
Requires: SUNWxwplt
BuildConflicts: SUNWlibsdl

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:		 %{_basedir}
%include default-depend.inc
Requires: %{name}


%prep
%setup -q -n SDL-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}                 \
            --mandir=%{_mandir}                 \
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sdl-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Apr 26 2007 - dougs@truemail.co.th
- Added BuildConflicts: SUNWlibsdl
* Tue Sep 26 2006 - halton.huo@sun.com
- Bump version to 1.2.11
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEsdl
- change to root:bin to follow other JDS pkgs.
* Thu Apr 6 2006 - damien.carbery@sun.com
- Move Build/Requires to be listed under base package to be useful.
* Wed Nov 09 2005 - glynn.foster@sun.com
- Initial spec
