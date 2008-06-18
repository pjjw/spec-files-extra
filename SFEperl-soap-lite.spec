#
# spec file for package SFEperl-soap-lite
#
# includes module(s): SOAP::Lite and muliple others like Apache::SOAP and
#                     XMLRPC::Lite.
#

%define module_version 0.710.07
%define module_name SOAP-Lite
%define module_name_major SOAP

%define perl_version 5.8.4

%include Solaris.inc
Name:                    SFEperl-soap-lite
Summary:                 %{module_name}-%{module_version} PERL module
Version:                 %{perl_version}.%{module_version}
Source:                  http://search.cpan.org/CPAN/authors/id/M/MK/MKUTTER/%{module_name}-%{module_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWperl584core
Requires:                SFEperl-version
Requires:                SFEperl-uri
BuildRequires:           SUNWperl584core
BuildRequires:           SFEperl-version
BuildRequires:           SFEperl-uri
BuildRequires:           SUNWsfwhea

#  Apache::Lite
#  SOAP::*
#  XMLRPC::Lite


%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version

%build
cd %{module_name}-%{module_version}
perl Makefile.PL \
     -n \
    UNINST=0 \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \

make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd %{module_name}-%{module_version}
make install


#remove: /usr/lib/i86pc-solaris-64int/perllocal.pod
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*.pl
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%{_prefix}/perl5/vendor_perl/%{perl_version}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*


%changelog
* Wed 18 Jun 2008 - daymobrew@users.sourceforge.net
- Initial spec file
