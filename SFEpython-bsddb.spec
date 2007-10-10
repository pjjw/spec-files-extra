#
# spec file for package SFEpython-bsddb
#
# includes module(s): pybsddb
#
%include Solaris.inc

%define src_url         http://superb-west.dl.sourceforge.net/sourceforge/pybsddb
%define src_name        bsddb3

Name:                    SFEpython-bsddb
Summary:                 Python wrappers for Berkeley DB
URL:                     http://pybsddb.sourceforge.net
Version:                 4.5.0
Source:                  %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWPython
BuildRequires:           SUNWPython-devel
Requires:                SFEbdb
BuildRequires:           SFEbdb

%define python_version  2.4

%prep
%setup -q -n %{src_name}-%{version}

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
%{_libdir}/python%{python_version}/vendor-packages/bsddb3

%changelog
* Thu Oct 11 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
