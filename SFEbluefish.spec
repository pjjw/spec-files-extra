#
# spec file for package SFEbluefish
#
# includes module(s): bluefish
#
%include Solaris.inc

Name:                    SFEbluefish
Summary:                 Bluefish, a powerful editor for experienced web designers.
Version:                 1.0.7
Source:                  http://www.bennewitz.com/bluefish/stable/source/bluefish-%{version}.tar.bz2
URL:                     http://bluefish.openoffice.nl/index.html
Patch1:                  bluefish-01-timeval.diff
Patch2:                  bluefish-02-debug_func.diff
Patch3:                  bluefish-03-update-mime.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWpcre
BuildRequires: SUNWpcre-devel
Requires: SUNWgnome-spell
Requires: SUNWgnome-libs
BuildRequires: SUNWgnome-libs-devel
Requires: SUNWlibC

%prep
%setup -q -n bluefish-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/gnu/include -I/usr/sfw/include -DANSICPP"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib -L/usr/gnu/lib -R/usr/gnu/lib"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/application-registry
%{_datadir}/application-registry/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/bluefish
%ghost %attr (0755, root, root)  %{_datadir}/mime
%dir %attr (0755, root, other) %{_datadir}/mime-info
%{_datadir}/mime-info/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%changelog
* Tue Oct 16 2007 - laca@sun.com
- add /usr/gnu to search paths for the indiana build
* Thu Mar 29 2007 - daymobrew@users.sourceforge.net
- Change Requires of SUNWaspell to SUNWgnome-spell. Former has been obsoleted.
* Wed Jan 24 2007 - daymobrew@users.sourceforge.net
- s/SFEpcre/SUNWpcre/ because SUNWpcre is in Vermillion Devel.
* Fri Jan 07 2007 - daymobrew@users.sourceforge.net
- Bump to 1.0.7. Update source url.
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEbluefish
- change to root:bin to follow other JDS pkgs.
* Mon Jan 30 2006 - glynn.foster@sun.com
- Initial version
