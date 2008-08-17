#
# spec file for package SFEperl-crypt_idea
#
# includes module(s): Crypt-IDEA perl module

%include Solaris.inc

%define crypt_idea_version 1.08 
%define perl_version 5.8.4

Name:                    SFEperl-crypt-idea
Summary:                 Crypt-%{crypt_idea_version} PERL module
Version:                 %{perl_version}.%{crypt_idea_version}
Source:                  http://www.cpan.org/modules/by-module/Crypt/Crypt-IDEA-%{crypt_idea_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
Group:                   Development
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWperl584core
BuildRequires:           SUNWperl584core
BuildRequires:           SUNWsfwhea

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version

%build
cd Crypt-IDEA-%{crypt_idea_version}
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd Crypt-IDEA-%{crypt_idea_version}
make install
rm -rf $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/Crypt/._test.pl
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/Crypt
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/Crypt/*.pm
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/Crypt/*.pod
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sat Aug 17 2008 - rafael.alfaro@gmail.com
- Add license and group
* Thu Jul 06 2008 - rafael.alfaro@gmail.com
- Initial spec file 
