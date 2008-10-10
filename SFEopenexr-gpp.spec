#
# spec file for package SFEopenexr.spec
#
# includes module(s): openexr
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	openexr
%define src_url		http://download.savannah.nongnu.org/releases/openexr

Name:                   SFEopenexr-gpp
Summary:                high dynamic-range (HDR) image file format
Version:                1.6.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEilmbase-gpp-devel
Requires: SFEilmbase-gpp

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


ln -s `which automake-1.9` automake
ln -s `which aclocal-1.9` aclocal
export PATH=$PWD:$PATH
/usr/bin/echo "#! /bin/sh">/tmp/g++
/usr/bin/echo "`which g++` -R%_cxx_libdir \044*">>/tmp/g++
chmod 755 /tmp/g++

X11LIBS="-L/usr/X11/lib -R/usr/X11/lib"
SFWLIBS="-L/usr/sfw/lib -R/usr/sfw/lib"
export CPPFLAGS="-I/usr/X11/include"
export CXX=/tmp/g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export LDFLAGS="$X11LIBS $SFWLIBS -lstdc++ -R%_cxx_libdir -L%_cxx_libdir"
export LD_OPTIONS="-i"
export PKG_CONFIG_PATH="%_cxx_libdir/pkgconfig:$PKG_CONFIG_PATH"
bash ./bootstrap
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_cxx_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 

#            --disable-rpath		\
%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_cxx_libdir}/lib*.*a
rm -r $RPM_BUILD_ROOT%{_datadir}
rm -r $RPM_BUILD_ROOT%{_includedir}
rm -r $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_cxx_libdir}
%dir %attr (0755,root,other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*.pc

%changelog
* Thu Oct  9 2008 - markgraf@med.ovgu.de
- Initial version based on SFEopenexr.spec
  reworked to put libs into /usr/lib/g++/<g++-version>/
  share includes and binaries with SUNWopenexr
