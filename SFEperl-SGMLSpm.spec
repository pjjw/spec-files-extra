#
# spec file for package SFEperl-SGMLpm
#
# includes module(s): SGMLpm perl module
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define SGMLpm_version 1.03ii
%define perl_version 5.8.4
%define perldir %(perl -V:installvendorlib| awk -F\' '{ print $2 }')
%define src_url http://search.cpan.org/CPAN/authors/id/D/DM/DMEGG


Name:                    SFEperl-SGMLpm
Summary:                 Perl library for parsing the output of nsgmls
Version:                 %{perl_version}.%{SGMLpm_version}
Source:                  %{src_url}/SGMLSpm-%{SGMLpm_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
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
%setup -n SGMLSpm

%build

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT

mkdir -p $DESTDIR/usr/bin
mkdir -p $DESTDIR/%{perldir}

CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC \
make install_system BINDIR=${DESTDIR}/usr/bin PERL5DIR=${DESTDIR}/%{perldir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{perldir}/SGMLS.pm
%{perldir}/SGMLS/Output.pm
%{perldir}/SGMLS/Refs.pm
%{perldir}/skel.pl

%changelog
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec file
