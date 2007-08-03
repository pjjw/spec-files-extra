#
# spec file for package SFElibdts
#
# includes module(s): libdts
#
%include Solaris.inc

Name:                    SFElibdts
Summary:                 libdts  - a free library for decoding DTS Coherent Acoustics streams
Version:                 0.0.2
Source:                  http://download.videolan.org/pub/videolan/libdca/%{version}/libdca-%{version}.tar.gz
Patch1:			 libdts-01-sigtype.diff
#Patch2:                  libdts-02-picflags.diff
Patch2:                  libdts-02-shared.diff
Patch3:                  libdts-03-opt.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libdts-%version
%patch1 -p1
#%patch2 -p1 -b .pic
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -KPIC"

aclocal $ACLOCAL_FLAGS
libtoolize --force
autoheader
automake
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Fri Aug  3 2007 - dougs@truemail.co.th
- Build a shared library
* Sun Jan 21 2007 - laca@sun.com
- add patch picflags.diff
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibdts
- changed to root:bin to follow other JDS pkgs.
- moved lib*.a to -devel
- added dependencies
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
