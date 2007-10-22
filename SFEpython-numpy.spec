#
# spec file for package SFEpython-numpy
#
# includes module(s): numpy
#
%include Solaris.inc

%define  version_long   1.0.3.1

Name:                    SFEpython-numpy
Summary:                 Numerical processing extensions to the python programming language
URL:                     http://numpy.scipy.org/
Version:                 %{version_long}
Source:                  http://internap.dl.sourceforge.net/sourceforge/numpy/numpy-%{version_long}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           SUNWPython-devel
Requires:                SUNWPython

%define python_version  2.4

%prep
%setup -q -n numpy-%version

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages/

%changelog
* Mon Oct 22 2007 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 1.0.3.1

* Sun Sep 02 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
