#
# spec file for package SFEsauerbraten.spec
#
# includes module(s): sauerbraten
#
%include Solaris.inc

%define src_name	sauerbraten
%define src_url		http://nchc.dl.sourceforge.net/sourceforge/sauerbraten
%define src_edition	spring_edition_linux

Name:                   SFEsauerbraten
Summary:                Sauerbraten game engine
Version:                2007_04_15
Source:                 %{src_url}/%{src_name}_%{version}_%{src_edition}.tar.bz2
Patch1:			sauerbraten-01-solaris.diff
Patch2:			sauerbraten-02-startup.diff
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

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd src
export CXX=/usr/sfw/bin/g++
export CXXOPTFLAGS="-O3 -fno-omit-frame-pointer"
export LD_OPTIONS="-i -L/usr/X11/lib -R/usr/X11/lib"
make install

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sauerbraten
chmod 755 sauerbraten_unix
cp -p sauerbraten_unix $RPM_BUILD_ROOT%{_bindir}/sauerbraten
/usr/bin/tar fcp $RPM_BUILD_ROOT%{_datadir}/sauerbraten/data.tar README.html bin_unix config.cfg data packages docs

%post
cd ${BASEDIR}/share/sauerbraten
/usr/bin/tar fxp data.tar || exit 2
rm data.tar || exit 2
removef $PKGINST `pwd`/data.tar || exit 2
cd ..
chown -R root:bin sauerbraten
installf -f $PKGINST || exit 2

%preun
rm -rf ${BASEDIR}/share/sauerbraten

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/sauerbraten

%changelog
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version
