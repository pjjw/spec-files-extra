#
# spec file for package SFEwesnoth-dev.spec
#
%include Solaris.inc

%define _basedir /opt/games
%define _bindir %{_basedir}/bin
%define _datadir %{_basedir}/share
%define _mandir %{_datadir}/man
%define _libdir %{_basedir}/lib

%define _pythonlibdir /usr/lib

%define _docdir %{_basedir}/share/doc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    	SFEwesnothDev
Summary:                 	Battle for Wesnoth is a fantasy turn-based strategy game (development version)
Version:                 	1.5.0a
Source:                  	%{sf_download}/wesnoth/wesnoth-%{version}.tar.bz2
#Patch1:                         wesnoth-01-fixheaders.diff
#Patch2:                         wesnoth-02-fixgccextension.diff
#Patch3:                         wesnoth-03-fixgccism.diff
Patch4:                         wesnoth-04-fixlocale.diff
Patch5:                         wesnoth-05-fixconfigure.diff
#Patch6:                         wesnoth-06-fixundefsymbol.diff
#Patch7:                         wesnoth-07-fixundef2.diff
#Patch8:                          wesnoth-08-fixconst.diff
Patch9:							wesnoth-09-fixrand.diff
Patch10:						wesnoth-10-fixstd.diff
Patch11:						wesnoth-11-fixstrict.diff
Patch12:						wesnoth-12-fixmisshpp.diff
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
Requires:               SFEboost
Requires:		SUNWPython

%prep
%setup -q -n wesnoth-1.5.0
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
%patch4 -p1
%patch5 -p1
#%patch6 -p1
#%patch7 -p1
#%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CXXFLAGS="-O3 -library=stlport4 -staticlib=stlport4 -norunpath -features=tmplife -features=tmplrefstatic -features=extensions"
#export CXXFLAGS="%cxx_optflags"
#export LDFLAGS="%_ldflags -lsocket -lnsl"
export LDFLAGS="-library=stlport4 -staticlib=stlport4 -lsocket -lnsl -lboost_iostreams -L. -R."

# Cause configure script check for C compilers, but the build doesn't use any
#  of C compilers and cc doesn't eat -library=stlport4 and other options.
#  I defined cc as C++ compiler, until it will be fixed cleaner
export CC=$CXX
export CC32=$CXX32
export CC64=$CXX64

autoconf

export MSGFMT=/usr/gnu/bin/msgfmt
#export GMSGFMT=/usr/gnu/bin/msgfmt

./configure --program-suffix='-dev' 		\
            --prefix=%{_basedir}			\
            --bindir=%{_bindir}				\
            --datadir=%{_datadir}			\
            --mandir=%{_mandir}				\
            --libdir=%{_libdir}				\
            --htmldir=%{_docdir}			\
            --enable-editor                     	\
			--enable-shared						\
            --with-preferences-dir=".wesnoth-dev" 	\
            --enable-python-install     \
    	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

# rename python package directory to not colide with stable version
mv "$RPM_BUILD_ROOT%{_pythonlibdir}/python2.4/site-packages/wesnoth" "$RPM_BUILD_ROOT%{_pythonlibdir}/python2.4/site-packages/wesnoth-dev"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
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
%defattr (755, root, sys)
%dir %attr (0755, root, bin) %{_pythonlibdir}
%dir %attr (0755, root, bin) %{_pythonlibdir}/python2.4
%dir %attr (0755, root, bin) %{_pythonlibdir}/python2.4/site-packages
%dir %attr (0755, root, bin) %{_pythonlibdir}/python2.4/site-packages/wesnoth-dev
%{_pythonlibdir}/python2.4/site-packages/wesnoth-dev/*

%changelog
* Tue May 01 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Initial version
- This package deliver development version of wesnoth - more features,
-   more often new version and most of time it's enough stable for playing 
