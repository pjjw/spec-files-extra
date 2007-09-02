#
# spec file for package SFEpython-psycopg2
#
# includes module(s): psycopg2
#
%include Solaris.inc

Name:                    SFEpython-psycopg2
Summary:                 A PostgreSQL database adapter for the Python programming language
URL:                     http://www.initd.org/tracker/psycopg/wiki/PsycopgTwo
Version:                 2.0.6
Source:                  http://initd.org/pub/software/psycopg/psycopg2-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           SUNWPython-devel
BuildRequires:           SUNWpostgr-devel
Requires:                SUNWPython
Requires:                SUNWpostgr

%define python_version  2.4

%prep
%setup -q -n psycopg2-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages/psycopg2/

%changelog
* Sat Sep 02 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
