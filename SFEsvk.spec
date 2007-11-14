#
# spec file for package SFEsvk
#
# includes module(s): SVK
#

%include Solaris.inc

%define perl_version 5.8.4

Name:                    SFEsvk
Summary:                 svk decentralized version control system
Version:                 2.0.2
Source:                  http://search.cpan.org/CPAN/authors/id/C/CL/CLKAO/SVK-v%{version}.tar.gz
Patch1:                  svk-01-module-versions.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:  SUNWperl584core
Requires:       SUNWperl584core
Requires:       SUNWsvn
Requires:       SUNWneon
Requires:       SFEperl-algorithm-annotate
Requires:       SFEperl-algorithm-diff
Requires:       SFEperl-app-cli
Requires:       SFEperl-class-accessor
Requires:       SFEperl-class-autouse
Requires:       SFEperl-class-data-inherit
Requires:       SFEperl-clone
Requires:       SFEperl-compress-zlib
Requires:       SFEperl-data-hierarchy
Requires:       SFEperl-file-type
Requires:       SFEperl-freezethaw
Requires:       SFEperl-io-digest
Requires:       SFEperl-io-dynamic
Requires:       SFEperl-io-eol
Requires:       SFEperl-io-pager
Requires:       SFEperl-io-symlink
Requires:       SFEperl-list-moreutils
Requires:       SFEperl-locale-mt-simple
Requires:       SFEperl-locale-mt-lexicon
Requires:       SFEperl-log-log4perl
Requires:       SFEperl-path-class
Requires:       SFEperl-pod-escapes
Requires:       SFEperl-pod-simple
Requires:       SFEperl-svn-mirror
Requires:       SFEperl-svn-simple
Requires:       SFEperl-term-readkey
Requires:       SFEperl-universal-require
Requires:       SFEperl-uri
Requires:       SFEperl-version
Requires:       SFEperl-yaml-syck

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif

%prep
%setup -q -n SVK-v%{version}
%patch1 -p1

%build
# XXX
# workaround for CR 6612347

LD_PRELOAD=libneon.so \
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
    
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
make install

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

# XXX
# workaround for CR 6612347
mv $RPM_BUILD_ROOT%{_bindir}/svk $RPM_BUILD_ROOT%{_bindir}/svk.real
echo "#!/bin/sh" > $RPM_BUILD_ROOT%{_bindir}/svk
echo "LD_PRELOAD=libneon.so; export LD_PRELOAD" >> $RPM_BUILD_ROOT%{_bindir}/svk
echo "exec svk.real \"\$@\"" >> $RPM_BUILD_ROOT%{_bindir}/svk
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/svk

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%{_prefix}/perl5/vendor_perl/%{perl_version}/*.pm
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/SVK
%{_prefix}/perl5/vendor_perl/%{perl_version}/SVK/*
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Wed Nov 14 2007 - trisk@acm.jhu.edu
- Fix typo in wrapper script
* Tue Nov 13 2007 - trisk@acm.jhu.edu
- Initial spec
