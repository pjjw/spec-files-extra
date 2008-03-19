#
# spec file for package SFEsynergy.spec
#
# includes module(s): synergy
#

%include Solaris.inc
Name:                    SFEsynergy
Summary:                 Mouse and keyboard sharing utility
Version:                 1.3.1
Release:                 1
Source:                  %{sf_download}/synergy2/synergy-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
Buildroot:               %{_tmppath}/%{name}-%{version}-build
Patch1:                  synergy-01-suncc-compilation.diff
%include default-depend.inc
Requires: SUNWxwrtl

%description
Synergy lets you easily share a single mouse and keyboard between
multiple computers with different operating systems, each with its
own display, without special hardware.  It's intended for users
with multiple computers on their desk since each system uses its
own display.

%prep
%setup -q -n synergy-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=/usr
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# FIXME: install a default configuration file
#mkdir -p $RPM_BUILD_ROOT/etc
#cp -p examples/synergy.conf $RPM_BUILD_ROOT%{_sysconfdir}/synergy.conf
# TODO: Should I strip the files ?
strip -x $RPM_BUILD_ROOT/usr/bin/synergyc
strip -x $RPM_BUILD_ROOT/usr/bin/synergys

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
#%config(noreplace) %attr (0755, root, root) %{_sysconfdir}/synergy.conf

%changelog
* Wed Mar 19 2008 Doualot Nicolas <nicolas@slubman.info>
- Initial import

