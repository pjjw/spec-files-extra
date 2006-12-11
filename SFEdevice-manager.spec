#
# spec file for package SFEdevice-manager
#
# includes module(s): device-manager
#

%include Solaris.inc
%define python_version 2.4

Name:         SFEdevice-manager
License:      Other
Group:        System/GUI
Version:      0.5.8.1
Summary:      Device-manager is a GUI interface provided by hal to display information about devices.
Source:       http://people.freedesktop.org/~david/dist/hal-%{version}.tar.gz
URL:          http://www.freedesktop.org/wiki/Software_2fhal
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SUNWPython
BuildRequires: SUNWhal
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-python-libs
Requires: SUNWPython
Requires: SUNWhal

%prep
%setup -q -n hal-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
./configure --prefix=%{_prefix} \
			--datadir=%{_datadir}

%install
rm -rf $RPM_BUILD_ROOT
cd tools/device-manager
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_datadir}/hal/device-manager/*.pyo

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%{_bindir}/hal-device-manager
%{_datadir}/hal/device-manager/*

%changelog
* Wed Nov 22 2006 - jedy.wang@sun.com
- Initial spec
