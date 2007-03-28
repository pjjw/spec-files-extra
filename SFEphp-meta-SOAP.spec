#   
#
%include Solaris.inc

%define topcat1 SOAP
%define Pname1 %{topcat1}
%define Pvers1 0.10.1

%define topcat2 Net
%define Pname2 %{topcat2}_URL
%define Pvers2 1.0.14

%define topcat3 Net
%define Pname3 %{topcat3}_Socket
%define Pvers3 1.0.6

%define topcat4 HTTP
%define Pname4 %{topcat4}_Request
%define Pvers4 1.4.0

Name:                SFEphp-meta-SOAP
Summary:             PHP meta package: SOAP and its 3 (PEAR) dependencies
Version:             0.0.1
Source1:             http://pear.php.net/get/SOAP-0.10.1.tgz
Source2:             http://pear.php.net/get/Net_URL-1.0.14.tgz
Source3:             http://pear.php.net/get/Net_Socket-1.0.6.tgz
Source4:             http://pear.php.net/get/HTTP_Request-1.4.0.tgz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEphp
Requires: SFEphp

%define phplibdir %(pear config-get php_dir || echo "undefined")

%prep
%setup -c -T
%setup -D -a1 -T
mv package.xml %{Pname1}-%{Pvers1}/%{Pname1}.xml
%setup -D -a2 -T
mv package.xml %{Pname2}-%{Pvers2}/%{Pname2}.xml
%setup -D -a3 -T
mv package.xml %{Pname3}-%{Pvers3}/%{Pname3}.xml
%setup -D -a4 -T
mv package.xml %{Pname4}-%{Pvers4}/%{Pname4}.xml

%build
exit 0

%install
rm -rf $RPM_BUILD_ROOT
cd %{Pname1}-%{Pvers1}
pear install -n -P $RPM_BUILD_ROOT %{Pname1}.xml
install -D %{Pname1}.xml $RPM_BUILD_ROOT%{phplibdir}/manifest/%{Pname1}.xml
cd ..

cd %{Pname2}-%{Pvers2}
pear install -n -P $RPM_BUILD_ROOT %{Pname2}.xml
install -D %{Pname2}.xml $RPM_BUILD_ROOT%{phplibdir}/manifest/%{Pname2}.xml
cd ..

cd %{Pname3}-%{Pvers3}
pear install -n -P $RPM_BUILD_ROOT %{Pname3}.xml
install -D %{Pname3}.xml $RPM_BUILD_ROOT%{phplibdir}/manifest/%{Pname3}.xml
cd ..

cd %{Pname4}-%{Pvers4}
pear install -n -P $RPM_BUILD_ROOT %{Pname4}.xml
install -D %{Pname4}.xml $RPM_BUILD_ROOT%{phplibdir}/manifest/%{Pname4}.xml
cd ..

cd $RPM_BUILD_ROOT/%{phplibdir}
rm .depdb .depdblock .filemap .lock
rm -r .channels .registry

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin; export PATH' ;
  echo 'pear install -n -r %{phplibdir}/manifest/%{Pname1}.xml'
  echo 'pear install -n -r %{phplibdir}/manifest/%{Pname2}.xml'
  echo 'pear install -n -r %{phplibdir}/manifest/%{Pname3}.xml'
  echo 'pear install -n -r %{phplibdir}/manifest/%{Pname4}.xml'
  echo 'exit' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE
  
%preun
( echo 'PATH=/usr/bin; export PATH' ;
  echo 'pear uninstall -n -r %{Pname1}'
  echo 'pear uninstall -n -r %{Pname2}'
  echo 'pear uninstall -n -r %{Pname3}'
  echo 'pear uninstall -n -r %{Pname4}'
  echo 'exit' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{phplibdir}
%dir %attr (0755, root, bin) %{phplibdir}/manifest
%{phplibdir}/manifest/*.xml
%dir %attr (0755, root, bin) %{phplibdir}/%{topcat1}
%{phplibdir}/%{topcat1}/*
%dir %attr (0755, root, bin) %{phplibdir}/%{topcat2}
%{phplibdir}/%{topcat2}/*
# %dir %attr (0755, root, bin) %{phplibdir}/%{topcat3}
# %{phplibdir}/%{topcat3}/*
%dir %attr (0755, root, bin) %{phplibdir}/%{topcat4}
%{phplibdir}/%{topcat4}/*
%dir %attr (0755, root, bin) %{phplibdir}/docs
%{phplibdir}/docs/*
# %dir %attr (0755, root, bin) %{phplibdir}/data
# %{phplibdir}/data/*
# %dir %attr (0755, root, bin) %{phplibdir}/tests
# %{phplibdir}/tests/*

%changelog
* Wed Mar 28, 2007 - Eric Boutilier
- Initial spec
