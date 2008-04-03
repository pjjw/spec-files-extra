#
# spec file for package SUNWpcre
#
# includes module(s): PCRE
#
%include Solaris.inc

Name:                    SUNWpcre
Summary:                 PCRE - Perl Compatible Regular Expressions
Version:                 7.1
Source:                  ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n pcre-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir} --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-newline-is-crlf --disable-stack-for-recursion \
            --enable-utf8 --enable-unicode-properties
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
%{_bindir}/pcretest
%{_bindir}/pcregrep
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/pcre-config
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/pcre
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Thu Nov  1 2007 - damien.carbery@sun.com
- Set --norunpath so that internal dirs not in the libraries.
* Sat May 12 2007 - halton.huo@sun.com
- Bump tp 7.1
- Add %{_datadir}/doc/pcre to -devel
* Wed Mar 07 2007 - damien.carbery@sun.com
- Add configure options as suggested by Stefan Teleman.
  --enable-newline-is-crlf to handle newlines for data from other operating sys.
  --disable-stack-for-recursion to prevent pcre from blowing up the stack.
  --enable-utf8 and --enable-unicode-properties add Unicode/UTF-8 support.
* Wed Feb 21 2007 - dougs@truemail.co.th
- Bump to 7.0
* Mon Dec 11 2006 - damien.carbery@sun.com
- Renamed to SUNWpcre for inclusion in JDS spec-files.
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEpcre
- change to root:bin to follow other JDS pkgs.
* Mon Jan 30 2006 - glynn.foster@sun.com
- Initial version
