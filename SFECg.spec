#
# spec file for package SFECg.spec
#
# includes module(s): Cg
#
%include Solaris.inc

%define src_name	Cg
%define src_url		http://download.nvidia.com/developer/cg/Cg_1.5/beta2

Name:                   SFECg
Summary:                Nvidia Graphics Library
Version:                1.5_beta2
Source:                 %{src_url}/%{src_name}-%{version}_Solaris_x86.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%ifarch sparc
echo "Sorry no sparc version yet!"
exit 1
%endif

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT
gtar fxvz %SOURCE0
mv usr/local/Cg usr/share/Cg
rm -rf usr/local

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/cg.pc <<EOM
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_prefix}/lib
includedir=%{_prefix}/include

Name: Cg
Description: %{summary}
Version: %{version}
Cflags: -I%{_includedir}
Libs: -L%{_libdir} -R%{_libdir} -lCg -lCgGL -lGL
EOM


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/Cg
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
