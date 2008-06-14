#
# spec file for package SFElibdvdread
#
# includes module(s): libdvdread
#
%include Solaris.inc

Name:                    SFElibdvdread
Summary:                 libdvdread  - libdvdread provides a simple foundation for reading DVD video disks
Version:                 0.9.7
Source:                  ftp://ftp.linux.ee/pub/gentoo/distfiles/distfiles/libdvdread-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
buildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibdvdcss

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n libdvdread-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Jun 14 2008 - trisk@acm.jhu.edu
- Update download link
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibdvdread
- changed to root:bin to follow other JDS pkgs.
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
