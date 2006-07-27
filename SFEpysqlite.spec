#
# spec file for package SFEpysqlite
#
# includes module(s): pysqlite
#

%include Solaris.inc
Name:                    SFEpysqlite
Summary:                 Python DB-API 2.0 interface for the SQLite
%define 
%define major_version 2.3
Version:                 %{major_version}.2
Source:                  http://initd.org/pub/software/pysqlite/releases/%{major_version}/%{version}/pysqlite-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
Requires:                SFEsqlite3
BuildRequires:           SUNWPython-devel
BuildRequires:           SFEsqlite3-devel

%include default-depend.inc

%prep
%setup -q -n pysqlite-%version

%build
python setup.py build \
    --build-base=$RPM_BUILD_ROOT%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix $RPM_BUILD_ROOT%{_prefix}

rm -rf $RPM_BUILD_ROOT%{_prefix}/pysqlite2-doc

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/lib/python2.4
%dir %attr(0755, root, bin) %{_prefix}/lib/python2.4/site-packages
%dir %attr(0755, root, bin) %{_prefix}/lib/python2.4/site-packages/pysqlite2
%{_prefix}/lib/python2.4/site-packages/pysqlite2/*

%changelog
* Wed July 26 2006 - lin.ma@sun.com
- Initial spec file
