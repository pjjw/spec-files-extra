#
# spec file for package SFEassaultcube.spec
#
# includes module(s): assaultcube
#
%include Solaris.inc

%define src_name	AssaultCube
%define src_url		http://switch.dl.sourceforge.net/sourceforge/actiongame

Name:                   SFEassultcube
Summary:                AssaultCube Game
Version:                0.93
Source:                 %{src_url}/%{src_name}_v%{version}.tar.bz2
Patch1:			assaultcube-01-solaris.diff
Patch2:			assaultcube-02-conflict.diff
Patch3:			assaultcube-03-cmds.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-mixer
BuildRequires: SFEsdl-image-devel
Requires: SFEsdl-image

%prep
%setup -q -n %{src_name}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd source/src
export CXX=/usr/sfw/bin/g++
export CXXOPTFLAGS="-O3 -fno-omit-frame-pointer"
export LD_OPTIONS="-i -L/usr/X11/lib -R/usr/X11/lib"
make install

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/cube
chmod 755 assaultcube.sh assaultcube_server.sh
cp -p assaultcube.sh $RPM_BUILD_ROOT%{_bindir}/assaultcube
cp -p assaultcube_server.sh $RPM_BUILD_ROOT%{_bindir}/assaultcube_server
/usr/bin/tar fcp $RPM_BUILD_ROOT%{_datadir}/cube/data.tar README.html bot bin_unix config docs icon.ico packages

%post
cd ${BASEDIR}/share/cube
/usr/bin/tar fxp data.tar || exit 2
rm data.tar || exit 2
removef $PKGINST `pwd`/data.tar || exit 2
cd ..
chown -R root:bin cube
installf -f $PKGINST || exit 2

%preun
rm -rf ${BASEDIR}/share/cube

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/cube

%changelog
* Mon Jul 10 2007 - dougs@truemail.co.th
- Initial version
