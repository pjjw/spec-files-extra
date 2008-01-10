#
# spec file for package SFEzope-interface
#
# includes module(s): zope-interface
#

%include Solaris.inc
Name:                    SFEzope-interface
Summary:                 a separate distribution of the zope.interface package used in Zope 3
URL:                     http://zope.org/Wikis/Interfaces/FrontPage
Version:                 3.3.0
Source:                  http://www.zope.org/Products/ZopeInterface/%{version}/zope.interface-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%define python_version  2.4

%prep
%setup -q -n zope.interface-%version

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
#%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages


%changelog
* Thu Jan 10 2008  - Irene.huang@sun.com
- Initial spec
