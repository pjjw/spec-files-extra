#
# spec file for package SFEimagemagick.spec
#
# includes module(s): imagemagick
#
%include Solaris.inc

%define src_name	ImageMagick
%define src_url		ftp://ftp.imagemagick.org/pub/%src_name
%define major		6.3.4
%define minor		-4

Name:                   SFEimagemagick
Summary:                ImageMagick - Image Manipulation Utilities and Libraries
Version:                %major
Source:                 %{src_url}/%{src_name}-%{version}%{minor}.tar.bz2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

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

 
export CPPFLAGS="-I/usr/sfw/include/freetype2 -I/usr/X11/include"
export CFLAGS="%optflags -xCC -xc99=%none"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -L/usr/X11/lib -R/usr/sfw/lib:/usr/X11/lib"
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
%{_libdir}/%{src_name}-%{version}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/%{src_name}-%{version}
%{_mandir}
%dir %attr (0755,root,other) %{_datadir}/doc
%{_datadir}/doc/*
%{_prefix}/perl5

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version - version in sfw is too old :(
