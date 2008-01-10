#
# spec file for package SFEsetuptools
#
# includes module(s): setuptools
#

%include Solaris.inc
Name:                    SFEsetuptools
Summary:                 Download, build, install, upgrade, and uninstall Python packages -- easily!
URL:                     http://pypi.python.org/pypi/setuptools
Version:                 0.6c7
Source:                  http://pypi.python.org/packages/source/s/setuptools/setuptools-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%define python_version  2.4

%prep
%setup -q -n setuptools-%version

%build
python ./setup.py build
%install
rm -rf $RPM_BUILD_ROOT
python ./setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

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
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%{_libdir}/python%{python_version}/vendor-packages
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*


%changelog
* Thu Jan 10 2008  - Irene.huang@sun.com
- Initial spec
