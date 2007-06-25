#
# spec file for package SFEbcop
#


%include Solaris.inc

Name:                    SFEbcop
Summary:                 beryl compiz XML option parser
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Source0:                 http://www.gnome.org/~erwannc/compiz/bcop-snap-14-06-07.tar.gz
Patch1:                  bcop-01-solaris-port.diff
%description

%prep
rm -rf %name
mkdir %name
%setup -c -n %name
gtar -xzf %SOURCE0
%patch1 -p1

%build
# we just get the bits tarball from developer
cd compcomm/libraries/bcop
autoreconf -v --install
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir} \
	--localstatedir=%{_localstatedir} \
	--disable-scrollkeeper
make

%install
rm -rf $RPM_BUILD_ROOT
cd compcomm/libraries/bcop
make DESTDIR=$RPM_BUILD_ROOT install 

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, root) %{_libdir}
%{_libdir}/pkgconfig/*


%changelog
* Mon June 25 2007 - <erwann.chenede@sun.com>
- modification/polish for SFE integration
* Thu May 16 2007 - <chris.wang@sun.com>
- initial creation


