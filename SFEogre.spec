#
# spec file for package SFEogre.spec
#
# includes module(s): ogre
#
%include Solaris.inc

%define src_name	ogre-linux_osx
%define src_url		%{sf_download}/ogre

Name:                   SFEogre
Summary:                O-O Graphics Rendering Engine
Version:                v1-4-1
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:			ogre-01-rpath.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEopenexr-devel
Requires: SFEopenexr
BuildRequires: SFEcegui-devel
Requires: SFEcegui
BuildRequires: SFEfreeimage-devel
Requires: SFEfreeimage
BuildRequires: SFEzziplib-devel
Requires: SFEzziplib
BuildRequires: SFEcal3d-devel
Requires: SFEcal3d
BuildRequires: SFECg-devel
Requires: SFECg

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n ogrenew
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


ln -s `which automake-1.9` automake
ln -s `which aclocal-1.9` aclocal
export PATH=$PWD:$PATH

X11LIBS="-L/usr/X11/lib -R/usr/X11/lib"
SFWLIBS="-L/usr/sfw/lib -R/usr/sfw/lib"
export CPPFLAGS="-I/usr/X11/include"
export CXX=/usr/sfw/bin/g++
export CXXFLAGS="-O3 -fno-omit-frame-pointer"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags $X11LIBS $SFWLIBS -lstdc++"
export LD_OPTIONS="-i"
bash ./bootstrap
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-rpath		\
            --enable-shared		\
	    --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/OGRE

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Fixed links
* Mon May  7 2007 - dougs@truemail.co.th
- Initial version
