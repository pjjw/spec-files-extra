#
# spec file for package SFEswh-plugins
#
# includes module(s): swh-plugins
#

%include Solaris.inc
Name:                    SFEswh-plugins
Summary:                 LADSPA plugins
URL:                     http://plugin.org.uk/
Version:                 0.4.15
Source:                  http://plugin.org.uk/releases/%{version}/swh-plugins-%{version}.tar.gz
Patch1:                  swh-plugins-01-nowall.diff
Patch2:                  swh-plugins-02-fixinline.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: SFEladspa-devel
Requires: SFEladspa
BuildRequires: SFEfftw-devel
Requires: SFEfftw

%prep
%setup -q -n swh-plugins-%version

%patch1 -p1
%patch2 -p1

touch NEWS README AUTHORS ChangeLog COPYING

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I ."
export CFLAGS="%optflags"
#export CXXFLAGS="%cxx_optflags -lCrun -lCstd"
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"

libtoolize -f -c
aclocal $ACLOCAL_FLAGS -I .
autoconf -f
autoheader
automake -a -c -f

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --datadir=%{_datadir}       \
            --libdir=%{_libdir}         \
            --mandir=%{_mandir} 

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %dir %{_libdir}/ladspa
%{_libdir}/ladspa/*.so
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %dir %{_datadir}/ladspa
%{_datadir}/ladspa/*

%changelog
* Mon Mar 17 2008 - brian.cameron@sun.com
- Created with version 0.4.15
