#
# spec file for package SFEpython-mysql
#
# includes module(s): mysql
#
%include Solaris.inc

Name:                    SFEpython-mysql
Summary:                 A MySQL database adapter for the Python programming language
URL:                     http://sourceforge.net/projects/mysql-python
Version:                 1.2.2
Source:                  %{sf_download}/mysql-python/MySQL-python-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           SUNWPython-devel
BuildRequires:           SFEpython-setuptools
Requires:                SUNWPython
Requires:                SUNWmysqlu

%define python_version  2.4

%prep
%setup -q -n MySQL-python-%{version}

%build
export LDFLAGS="-R /usr/sfw/lib"
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
%{_libdir}/python%{python_version}/vendor-packages/

%changelog
* Sun Sep 02 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
