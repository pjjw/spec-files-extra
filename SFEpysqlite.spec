#
# spec file for package SFEpysqlite
#
# includes module(s): pysqlite
#
%define pythonver 2.4

%include Solaris.inc

Name:                    SFEpysqlite
Summary:                 Python DB-API 2.0 interface for the SQLite
%define 
%define major_version 2.3
Version:                 %{major_version}.5
Source:                  http://initd.org/pub/software/pysqlite/releases/%{major_version}/%{version}/pysqlite-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
Requires:                SFEsqlite
BuildRequires:           SUNWPython-devel
BuildRequires:           SFEsqlite-devel

%include default-depend.inc

%prep
%setup -q -n pysqlite-%version

%build
python setup.py build \
    --build-base=$RPM_BUILD_ROOT%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix $RPM_BUILD_ROOT%{_prefix}

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

rm -rf $RPM_BUILD_ROOT%{_prefix}/pysqlite2-doc

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/lib/python2.4
%dir %attr(0755, root, bin) %{_prefix}/lib/python2.4/vendor-packages
%dir %attr(0755, root, bin) %{_prefix}/lib/python2.4/vendor-packages/pysqlite2
%{_prefix}/lib/python2.4/vendor-packages/pysqlite2/*

%changelog
* Tue Oct 09 2007 - Brian.Cameron@sun.co
- Move module from site-packages to vendor-packages.
* Fri Oct 05 2007 - Brian.Cameron@sun.com
- Bump to 2.3.5
* Wed July 26 2006 - lin.ma@sun.com
- Initial spec file
