#
# spec file for package SFElibdvbpsi
#
# includes module(s): libdvbpsi
#
%include Solaris.inc

Name:                    SFElibdvbpsi
Summary:                 libdvbpsi  - a simple library designed for decoding and generation of MPEG TS and DVB PSI tables
Version:                 0.1.5
Source:                  http://download.videolan.org/pub/libdvbpsi/%{version}/libdvbpsi4-%{version}.tar.bz2
Patch1:			 libdvbpsi-01-configure.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libdvbpsi4-%version
%patch1 -p1

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
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibdvbpsi
- changed to root:bin to follow other JDS pkgs.
* Wed Feb 15 2004 - glynn.foster@sun.com
- Initial version
