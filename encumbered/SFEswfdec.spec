#
# spec file for package SFEswfdec
#
# includes module(s): swfdec
#
%include Solaris.inc

Name:                    SFEswfdec
Summary:                 Macromedia Flash Rendering Library
Version:                 0.4.1
Source:                  http://swfdec.freedesktop.org/download/swfdec/0.4/swfdec-%{version}.tar.gz
URL:                     http://swfdec.freedesktop.org/wiki/
Group:                   library/multimedia
Patch1:                  swfdec-01-build-fix.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWfirefox
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-media
Requires: SUNWlibms
Requires: SUNWliboil
Requires: SUNWlxml
Requires: SUNWmlib
Requires: SUNWxwrtl
Requires: SUNWzlib
Requires: SFElibmad
Requires: SFEffmpeg
BuildRequires: SUNWfirefox-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-media
BuildRequires: SUNWlibm
BuildRequires: SUNWliboil-devel
BuildRequires: SUNWmlibh
BuildRequires: SFElibmad-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n swfdec-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/include/firefox -I/usr/include/firefox/js"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int
export LDFLAGS="%_ldflags"

glib-gettextize -f 
libtoolize --copy --force
intltoolize --copy --force --automake
aclocal $ACLOCAL_FLAGS -I m4
autoheader
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --disable-mozilla-plugin

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/mozilla

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Sun Jan 14 2007 - laca@sun.com
- bump to 0.4.1; update %files
* Mon Jul 10 2006 - laca@sun.com
- rename to SFEswfdec
- update file attributes
- add missing deps
- disable firefox plugin because it hangs the browser
* Fri May  5 2006 - damien.carbery@sun.com
- Add gimp plugin to package.
* Thu Apr  6 2006 - damien.carbery@sun.com
- Update Build/Requires after check-deps.pl run.
* Fri Jan 13 2005 - glynn.foster@sun.com
- Initial spec file
