#
# spec file for package SFEimagemagick.spec
#
# includes module(s): imagemagick
#
%include Solaris.inc

Name:                   SFEgraphicsmagick
Summary:                GraphicsMagick - Image Manipulation Utilities and Libraries
Version:                1.1.10
Source:                 %{sf_download}/graphicsmagick/GraphicsMagick-%{version}.tar.bz2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%include perl-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n GraphicsMagick-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

 
export CPPFLAGS="-I/usr/sfw/include/freetype2 -I/usr/X11/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -L/usr/X11/lib -R/usr/sfw/lib -R/usr/X11/lib"
if [ "x`basename $CC`" = xgcc ]
then
	%error "Building this spec with GCC is not supported."
fi
export CFLAGS="%optflags -xCC"
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
find $RPM_BUILD_ROOT%{_libdir} -name lib\*.\*a -exec rm {} \;
site_perl=$RPM_BUILD_ROOT/usr/perl5/site_perl
vendor_perl=$RPM_BUILD_ROOT/usr/perl5/vendor_perl
mv $site_perl $vendor_perl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/GraphicsMagick-%{version}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/GraphicsMagick-%{version}
%dir %attr (0755,root,other) %{_datadir}/GraphicsMagick
%{_mandir}
%{_prefix}/perl5

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Jan 28 2008 - moinak.ghosh@sun.com
- Initial spec.
