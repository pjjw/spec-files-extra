#
# spec file for package SFElibhid.spec
#
# includes module(s): libhid
#
%include Solaris.inc

%define src_name	libhid
%define src_url		http://alioth.debian.org/frs/download.php/1958

Name:                   SFElibhid
Summary:                USB Human Interface Device user level driver library
Version:                0.2.16
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			libhid-01-tests.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

libtoolize --force --copy
aclocal -I m4
autoheader
automake --add-missing
autoconf --force

export CPPFLAGS="-D__FUNCTION__=__func__"
export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
export LD_OPTIONS="-i -z combreloc -z direct -L/usr/sfw/lib -R/usr/sfw/lib"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		\
	    --disable-werror		\
	    --disable-warnings

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Jul 10 2007 - dougs@truemail.co.th
- Initial version
