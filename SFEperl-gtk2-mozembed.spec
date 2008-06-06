#
# spec file for package SFEperl-gtk2-mozembed
#
# includes module(s): perl-gtk2-mozembed
#

%include Solaris.inc

%define tarball_version 0.06
%define perl_version 5.8.4

Name:                    SFEperl-gtk2-mozembed
Summary:                 Gtk2-MozEmbed-%{tarball_version} PERL module for Mozilla embedding widget.
Version:                 %{perl_version}.%{tarball_version}
Source:                  %{sf_download}/gtk2-perl/Gtk2-MozEmbed-%{tarball_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:  SUNWperl584core
Requires:       SUNWperl584core
Requires:		SUNWgnome-base-libs
Requires:		SFEperl-glib
Requires:		SFEperl-gtk2
Requires:		SFEperl-cairo
BuildRequires:	SFEperl-extutils-dep
BuildRequires:	SFEperl-extutils-pkg

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif

%prep
%setup -q	 -c -n %name-%version

%build
cd Gtk2-MozEmbed-%{tarball_version}
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
    
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD="$CC -R/usr/lib/firefox"

%install
rm -rf $RPM_BUILD_ROOT
cd Gtk2-MozEmbed-%{tarball_version}
make install

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Fri Jun 06 2008 - Andras Barna <andras.barna@gmail.com>
- Added "-R/usr/lib/firefox" to LD
* Sun Jan 28 2007 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Updated how version is defined.
* Fri Jan 12 2007 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec file
