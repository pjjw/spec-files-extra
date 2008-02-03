#
# spec file for package SFEperl-uri
#
# includes module(s): Curses perl module
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define curs_version 1.20
%define perl_version 5.8.4

Name:                    SFEperl-curses
Summary:                 Curses-%{curs_version} PERL module
Version:                 %{perl_version}.%{curs_version}
Source:                  http://search.cpan.org/CPAN/authors/id/G/GI/GIRAFFED/Curses-%{curs_version}.tgz
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
%setup -q            -c -n %name-%version

%build
cd Curses-%{curs_version}
export CURSES_VERBOSE="1"
export CURSES_LDFLAGS="%{gnu_lib_path} -lncurses -lmenu -lform -lpanel %picflags"
export CURSES_CFLAGS="-I%{gnu_inc} -I%{gnu_inc}/ncurses %optflags"

#export CURSES_PANEL_CFLAGS=${CURSES_CFLAGS}
#export CURSES_PANEL_LDFLAGS=${CURSES_LDFLAGS}
#export CURSES_MENU_CFLAGS=${CURSES_CFLAGS}
#export CURSES_MENU_LDFLAGS=${CURSES_LDFLAGS}
#export CURSES_FORM_CFLAGS=${CURSES_CFLAGS}
#export CURSES_FORM_LDFLAGS=${CURSES_LDFLAGS}

perl Makefile.PL PANELS MENUS FORMS \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%{gnu_lib_path} %picflags" OPTIMIZE="-I%{gnu_inc} -I%{gnu_inc}/ncurses %optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd Curses-%{curs_version}
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
* Mon Feb 04 2008 - moinak.ghosh@sun.com
- Initial spec.
