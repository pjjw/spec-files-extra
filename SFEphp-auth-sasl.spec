#   
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define topcat Auth
%define Pname %{topcat}_SASL

Name:                SFEphp-auth-sasl
Summary:             PHP package: Abstraction of SASL mechanism responses
Version:             1.0.2
URL:                 http://pear.php.net/package/%{Pname}
Source:              http://pear.php.net/get/%{Pname}-%{version}.tgz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEphp
Requires: SFEphp

%define phplibdir %(test -x /usr/bin/pear && pear config-get php_dir || echo "/undefined")

%prep
%setup -q -n %{Pname}-%version
mv ../package.xml .

%build
exit 0

%install
rm -rf $RPM_BUILD_ROOT
pear install -n -P $RPM_BUILD_ROOT package.xml
mv package.xml %{Pname}.xml
install -D %{Pname}.xml $RPM_BUILD_ROOT%{phplibdir}/manifest/%{Pname}.xml

cd $RPM_BUILD_ROOT/%{phplibdir}
rm .depdb .depdblock .filemap .lock
rm -r .channels .registry

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin; export PATH' ;
  echo 'retval=0';
  echo 'pear install -n -r %{phplibdir}/manifest/%{Pname}.xml || retval=1'
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE
  
%preun
( echo 'PATH=/usr/bin; export PATH' ;
  echo 'pear uninstall -n -r %{Pname}'
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{phplibdir}
%dir %attr (0755, root, bin) %{phplibdir}/manifest
%{phplibdir}/manifest/%{Pname}.xml
%dir %attr (0755, root, bin) %{phplibdir}/%{topcat}
%{phplibdir}/%{topcat}/*
# %dir %attr (0755, root, bin) %{phplibdir}/docs
# %{phplibdir}/docs/*
# %dir %attr (0755, root, bin) %{phplibdir}/data
# %{phplibdir}/data/*
# %dir %attr (0755, root, bin) %{phplibdir}/tests
# %{phplibdir}/tests/*

%changelog
* Thu Mar 29 2007 - Eric Boutilier 
- Fixed missing test in %define phplibdir
* Sat Mar 24 2007 - Eric Boutilier
- Initial spec
