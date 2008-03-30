#
# spec file for package SUNWimagick
#
# includes module(s): imagemagick
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
# DO NOT REMOVE NEXT LINE
# PACKAGE NOT ARC REVIEWED BY SUN JDS TEAM
#
%include Solaris.inc

Name:                    SUNWimagick
%define tarball_version  6.3.4
Summary:                 ImageMagick - Image Manipulation Utilities and Libraries %{tarball_version}
Version:                 11.10.1
%define im_rev -10
Source:                  ftp://ftp.imagemagick.org/pub/ImageMagick/ImageMagick-%{tarball_version}%{im_rev}.tar.bz2
# owner:laca type:feature date:2007-05-18
Patch1:                  imagemagick-01-ltdl.diff
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%define perl_version 5.8.4
%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int
%endif
%include default-depend.inc
Requires: SUNWbzip
Requires: SUNWfreetype2
Requires: SUNWgscr
Requires: SUNWjpg
Requires: SUNWperl584usr
Requires: SUNWpng
Requires: SUNWTiff
Requires: SUNWzlib
Requires: SUNWlxml
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWgnome-base-libs
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWpng-devel
BuildRequires: SUNWTiff-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name

%prep
%setup -q -n ImageMagick-%tarball_version
%patch1 -p1

%build
export CXXFLAGS="%cxx_optflags"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"
./configure --prefix=%{_prefix} \
            --disable-static \
            --mandir=%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/ImageMagick-*/modules*/coders/*.la
rm $RPM_BUILD_ROOT%{_libdir}/ImageMagick-*/modules*/filters/*.la
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la
mv $RPM_BUILD_ROOT/usr/perl5/site_perl $RPM_BUILD_ROOT/usr/perl5/vendor_perl
rm -rf $RPM_BUILD_ROOT/usr/perl5/*/lib

# compatibility symlinks in /usr/sfw/bin
mkdir -p $RPM_BUILD_ROOT/usr/sfw/bin
cd $RPM_BUILD_ROOT/usr/sfw/bin
for prog in animate composite conjure convert display identify import \
    mogrify motage; do
    ln -s ../../bin/$prog .
done

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{tarball_version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/ImageMagick*/config
%{_libdir}/ImageMagick*/modules-*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/[a-z]*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/ImageMagick-*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
#/usr/perl5/*/man/man3/Image::Magick.3
%dir %attr(0755, root, bin) %{_prefix}/perl5
%{_prefix}/perl5/%{perl_version}/man
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/Image
%dir %attr (0755, root, bin) /usr/sfw
%dir %attr (0755, root, bin) /usr/sfw/bin
/usr/sfw/bin/*
%if %is_s10
%dir %attr(0755, root, other) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto/*
%else
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto
%endif


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*-config
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sat Dec 22 2007 - patrick.ale@gmail.com
- Bump up im_rev to 10. im_rev 1 is N/A anymore.
* Fri Sep 28 2007 - laca@sun.com
- change SUNWxwrtl dep to SUNWgnome-base-libs
* Fri May 18 2007 - laca@sun.com
- bump to 6.3.4-1
- add patch ltdl.diff which makes it use .so modules instead of .la files
- fix %install so that modules are not removed
- set basedir to / to match SFW
- create backcompat symlinks in /usr/sfw/bin
* Thu Apr 26 2007 - laca@sun.com
- set CXX to $CXX -norunpath because libtool swallows this option sometimes
  and leaves compiler paths in the binaries
* Sun Jan 28 2007 - laca@sun.com
- update %files so that the attributes work on both s10 and nevada
* Sun Dec 03 2006 - damien.carbery@sun.com
- Revert to 6.2.5-5 because 'convert' cannot find png info (breaks 
  SUNWgnome-themes).
* Fri Dec 01 2006 - damien.carbery@sun.com
- Bump to 6.3.0-7. Remove '-lCrun -lCstd' from CXXFLAGS. Add 'make' to %build. 
* Mon Oct 16 2006 - damien.carbery@sun.com
- Remove the '-rf' from the 'rm *.la *.a' lines so that any changes to the
  module source will be seen as a build error and action can be taken.
* Sun Oct 08 2006 - damien.carbery@sun.com
- Unbump because it breaks gnome-themes.
* Sat Oct  7 2006 - laca@sun.com
- Bump to 6.2.9-8
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Wed Feb 15 2006 - damien.carbery@sun.com
- Correct perl perms to match those in other packages.
* Thu Dec  8 2005 - laca@sun.com
- renamed to SUNWimagick
* Thu Dec 08 2005 - damien.carbery@sun.com
- Bump to 6.2.5-5.
* Sat Oct 15 2005 - laca@sun.com
- created
