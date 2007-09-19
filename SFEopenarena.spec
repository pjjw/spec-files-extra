#
# spec file for package SFEopenarena.spec
#
# includes module(s): openarena
#
%include Solaris.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

%define src_name        ioq3-src-oa
%define src_version     070
%define patch_version   071
%define src_url         http://openarena.ws/rel
#%define mirror_url      http://download.tuxfamily.net/cooker/openarena/rel070

Name:                   SFEopenarena
Summary:                OpenArena - Fast-paced 3D first-person shooter based on ioquake3
Version:                0.7.1
URL:                    http://openarena.ws/
Source:                 %{src_url}/%{src_version}/%{src_name}.tar.bz2
Source1:                %{src_url}%{src_version}/oa%{src_version}.zip
#Source:                 %{mirror_url}/%{src_name}.tar.bz2
#Source1:                %{mirror_url}/oa%{src_version}.zip
Source2:                %{src_url}/%{patch_version}/oa%{patch_version}-patch.zip
Patch1:                 openarena-01-solaris.diff
Patch2:                 openarena-02-menudef.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
%ifarch i386 amd64
BuildRequires: SUNWxorg-mesa
%endif
BuildRequires: SUNWogg-vorbis-devel
BuildRequires: SFEcurl-devel
BuildRequires: SFEopenal-devel
Requires: SUNWogg-vorbis
Requires: SFEcurl
Requires: SFEopenal

%prep
%setup -q -c -n %{name}
%patch1 -p1
%patch2 -p1
unzip -o %{SOURCE1}
unzip -o %{SOURCE2}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=/usr/sfw/bin/gcc
make USE_CURL_DLOPEN=0 USE_OPENAL_DLOPEN=0 USE_LOCAL_HEADERS=0

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/openarena/baseq3
mkdir -p $RPM_BUILD_ROOT%{_libdir}/openarena/missionpack
mkdir -p $RPM_BUILD_ROOT%{_datadir}/openarena

Q3ARCH=$(uname -p)
cp build/release-sunos-$Q3ARCH/ioquake3.$Q3ARCH $RPM_BUILD_ROOT%{_libdir}/openarena/openarena.bin
cp build/release-sunos-$Q3ARCH/ioquake3-smp.$Q3ARCH $RPM_BUILD_ROOT%{_libdir}/openarena/openarena-smp.bin
cp build/release-sunos-$Q3ARCH/ioq3ded.$Q3ARCH $RPM_BUILD_ROOT%{_libdir}/openarena/openarena-server.bin
for prog in openarena openarena-smp openarena-server; do
  echo "#!/bin/sh" > $RPM_BUILD_ROOT%{_bindir}/$prog
  case prog in
    *-server)
    echo "exec %{_libdir}/openarena/${prog}.bin +set fs_basepath %{_datadir}/openarena \"\$@\"" >> $RPM_BUILD_ROOT%{_bindir}/$prog
    ;;
    *)
    echo "exec %{_libdir}/openarena/${prog}.bin +set fs_basepath %{_datadir}/openarena +set ttycon 0 \"\$@\"" >> $RPM_BUILD_ROOT%{_bindir}/$prog
    ;;
  esac
  chmod 0755 $RPM_BUILD_ROOT%{_bindir}/$prog
done

cp build/release-sunos-$Q3ARCH/baseq3/*.so $RPM_BUILD_ROOT%{_libdir}/openarena/baseq3
cp build/release-sunos-$Q3ARCH/missionpack/*.so $RPM_BUILD_ROOT%{_libdir}/openarena/missionpack

mkdir -p $RPM_BUILD_ROOT%{_datadir}/openarena/baseoa
cp openarena-0.7.0/baseoa/* $RPM_BUILD_ROOT%{_datadir}/openarena/baseoa
chmod 0644 $RPM_BUILD_ROOT%{_datadir}/openarena/baseoa/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/openarena
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/openarena

%changelog
* Wed Sep 19 2007 - trisk@acm.jhu.edu
- Initial spec
