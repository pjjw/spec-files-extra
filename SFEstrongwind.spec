#
# spec file for package SFEstrongwind
#
# includes module(s): strongwind
#

%include Solaris.inc
Name:                    SFEstrongwind
Summary:                 GUI test automation framework
URL:                     http://medsphere.org/projects/strongwind/
Version:                 0.9
Source:                  http://medsphere.org/projects/strongwind/strongwind-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires: SUNWgnome-base-libs
Requires: SUNWPython-extra

%define pythonver 2.4

%description
Strongwind is a GUI test automation framework.

%include default-depend.inc

%prep
%setup -q -n strongwind-%version

%build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python?.?/vendor-packages

%changelog
* Thu Oct 25 2007 - Brian Cameron <brian.cameron@sun.com>
- Created.
