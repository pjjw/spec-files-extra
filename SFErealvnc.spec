#
# spec file for package SFErealvnc
#
# includes module(s): realvnc
#
# Owner: laca
#
%include Solaris.inc

Name:                    SFErealvnc
Summary:                 realvnc - remote control software
Version:                 4.1.2
%define tarball_version  4_1_2
# download the source manually from http://www.realvnc.com/cgi-bin/download.cgi
Source:                  vnc-%{tarball_version}-unixsrc.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWxwplt
Requires: SUNWzlib
Requires: SUNWjpg
Requires: SUNWlibmsr
Conflicts: SFEtightvnc

%prep
%setup -q -n vnc-%{tarball_version}-unixsrc

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
cd unix
./configure \
    --prefix=%{_prefix} \
    --with-installed-zlib \
    --with-x
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd unix
mkdir -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_mandir}/man1
./vncinstall $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_mandir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sun Jun 10 2007 - laca@sun.com
- Initial spec
