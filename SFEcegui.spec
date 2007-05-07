#
# spec file for package SFEgui.spec
#
# includes module(s): cegui
#
%include Solaris.inc

%define src_name	CEGUI
%define src_url		http://nchc.dl.sourceforge.net/sourceforge/crayzedsgui

Name:                   SFEcegui
Summary:                Crazy Eddies Graphics Library
Version:                0.5.0
Source:                 %{src_url}/%{src_name}-%{version}b.tar.gz
Patch1:			cegui-01-dlopen.diff
Patch2:			cegui-02-gtk.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: SUNWpcre

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


X11LIBS="-L/usr/X11/lib -R/usr/X11/lib"
SFWLIBS="-L/usr/sfw/lib -R/usr/sfw/lib"
export CPPFLAGS="-I/usr/X11/include"
export CXX=/usr/sfw/bin/g++
export CXXFLAGS="-O3 -fno-omit-frame-pointer"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags $X11LIBS $SFWLIBS -lstdc++"
export LD_OPTIONS="-i"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon May  7 2007 - dougs@truemail.co.th
- Initial version
