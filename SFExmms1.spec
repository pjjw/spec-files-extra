#
# spec file for package SFExmms2
#
# includes module(s): xmms2
#

%include Solaris.inc

Name:                    SFExmms1
Summary:                 X Multimedia System
Version:                 1.2.11
Source:                  http://www.xmms.org/files/1.2.x/xmms-%{version}.tar.bz2
Patch1:  		  xmms1-01-rand.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWGtku
Requires: SUNWGtkr
Requires: SUNWgnome-audio
BuildRequires: SUNWsfwhea
BuildRequires: SFEmpg321
BuildRequires: SUNWgnome-audio-devel
BuildRequires: oss

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWsfwhea
Requires: oss

%package encumbered
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEmpg321

%prep
%setup -q -n xmms-%{version}
%patch1 -p1 -b .patch01

%build
export CFLAGS="%optflags -fpic -I/usr/X11/include -I/usr/gnu/include -I/usr/gnu/include/sasl -I/usr/sfw/include -D__C99FEATURES__ -D__EXTENSIONS__ -DINSTALLPREFIX=\\\"%{_prefix}\\\""
export LDFLAGS="-L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -lc -lsocket -lnsl -lgdk"

./configure -prefix %{_prefix} \
           --mandir %{_mandir} \
           --sysconfdir %{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --with-extra-includes="/usr/X11/include:/usr/gnu/include:/usr/gnu/include/sasl:/usr/sfw/include:usr/include/pcre"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

# Generate libraries list since we have to separate
# out a few encumbered files.
#
echo "%defattr (-, root, bin)" > %{_builddir}/xmms-%version/xmms_libfiles
echo "%dir %attr (0755, root, bin) %{_libdir}" >> %{_builddir}/xmms-%version/xmms_libfiles
(cd ${RPM_BUILD_ROOT}; find ./%{_libdir}/* \( -type f -o -type l \) | \
    egrep -v "mpg|mpeg" | sed 's/^\.\///' \
    >> %{_builddir}/xmms-%version/xmms_libfiles)


%clean
rm -rf $RPM_BUILD_ROOT

%files -f xmms_libfiles
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xmms
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*
%{_datadir}/aclocal

%files devel
%defattr (-, root, bin)
%{_includedir}

%files encumbered
%defattr (-, root, bin)
%{_libdir}/xmms/Input/libmpg*

%changelog
* Wed Apr 30 2008 - andras.barna@gmail.com
- Add patch which fixes crash when pressing random.
* Sun Jan 20 2008 - moinak.ghosh@sun.com
- Initial spec.
