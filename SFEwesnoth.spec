#
# spec file for package SFEwesnoth.spec
#
%include Solaris.inc

# For binary packages on wesnoth.org
#%define _basedir /opt/games
#%define _bindir %{_basedir}/bin
#%define _datadir %{_basedir}/share
#%define _mandir %{_datadir}/man
#%define _libdir %{_basedir}/lib

%define _docdir %{_basedir}/share/doc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    	SFEwesnoth
Summary:                 	Battle for Wesnoth is a fantasy turn-based strategy game
Version:                 	1.3.10
Source:                  	http://kent.dl.sourceforge.net/sourceforge/wesnoth/wesnoth-%{version}.tar.bz2
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
BuildRequires:		SFEsdl-mixer-devel
BuildRequires:		SFEsdl-ttf-devel
BuildRequires:		SFEsdl-net-devel
BuildRequires:		SFEsdl-image-devel
Requires:		SFEsdl-mixer
Requires:		SFEsdl-ttf
Requires:		SFEsdl-net
Requires:		SFEsdl-image
Requires:		SUNWPython

%prep
%setup -q -n wesnoth-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC="gcc"
export CXX="g++"
export CFLAGS="-I/usr/sfw/include"
export CXXFLAGS="-I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -lsocket -lnsl"

./configure --prefix=%{_basedir}			\
            --bindir=%{_bindir}				\
            --datadir=%{_datadir}			\
            --mandir=%{_mandir}				\
            --libdir=%{_libdir}				\
            --htmldir=%{_docdir}			\
            --with-localedir=%{_localedir}		\
            --enable-dummy-locales			\
            --enable-shared				\
            --enable-editor                     	\
            --with-preferences-dir=".wesnoth-dev" 	\
	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%defattr (-, root, other)
%dir %attr (-, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/wesnoth
%{_datadir}/wesnoth/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/wesnoth
%{_docdir}/wesnoth/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%dir %attr (0755, root, bin) %{_libdir}/python2.4/site-packages
%dir %attr (0755, root, bin) %{_libdir}/python2.4/site-packages/wesnoth
%{_libdir}/python2.4/site-packages/wesnoth/*


%changelog
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Sun Nov 11 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.10
* Fri Oct 19 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.9
- add html documentation
* Wed Sep 19 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.8
* Thu Sep 6 2007 Petr Sobotka <sobotkap@centrum.cz>
- Initial version
