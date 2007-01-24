#
# spec file for package SFEcherokee
#
# includes module(s): cherokee
#

%include Solaris.inc

Name:                    SFEcherokee
Summary:                 cherokee - Fast, flexible, lightweight web server
Version:                 0.5.5
Source:                  http://www.cherokee-project.com/download/0.5/%{version}/cherokee-%{version}.tar.gz
URL:                     http://www.cherokee-project.com/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnutls
Requires: SUNWlibgpg-error
Requires: SUNWpcre
Requires: %{name}-root
BuildRequires: SUNWgnutls-devel
BuildRequires: SUNWpcre-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel          
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n cherokee-%version

%build
export CFLAGS="%optflags -I%{_includedir}"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}                 \
            --enable-os-string="OpenSolaris"    \
            --enable-pthreads                   \
            --libexecdir=%{_libexecdir}         \
            --datadir=%{_datadir}               \
            --mandir=%{_mandir}                 \
            --infodir=%{_infodir}               \
            --sysconfdir=%{_sysconfdir}         \
            --localstatedir=%{_localstatedir}   \
            --with-wwwroot=%{_localstatedir}/cherokee
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/cherokee/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/cherokee/lib*.la

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/network/
cp http-cherokee.xml ${RPM_BUILD_ROOT}/var/svc/manifest/network/http-cherokee.xml

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/cherokee
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/cherokee
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/cherokee
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*


%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/cherokee/*
%defattr (0755, root, sys)
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/network/http-cherokee.xml

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Wed Jan 24 2007 - daymobrew@users.sourceforge.net
- s/SFEpcre/SUNWpcre/ because SUNWpcre is in Vermillion Devel.
* Wed Jan  3 2007 - laca@sun.com
- bump to 0.5.5 (note: 0.5.6 doesn't compile on Solaris)
- update download urls
* Fri Jun 23 2006 - laca@sun.com
- renamed to SFEcherokee
- updated file attributes
- removed the procedural scripts and added the manifest file to the manifest
  class
* Fri May 05 2006 - damien.carbery@sun.com
- Bump to 0.5.3.
* Thu Mar 30 2006 - damien.carbery@sun.com
- Add site URL and bump to 0.5.0.
* Wed Jan 25 2006 - rodrigo.fernandez-vizarra@sun.com
- Added SMF definition file install/removal
* Tue Jan 17 2006 - damien.carbery@sun.com
- Created.
