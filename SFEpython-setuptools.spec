#
# spec file for package SFEpython-setuptools
#
# includes module(s): setuptools
#
%define oname setuptools
%define name python-%oname
%define version 0.6c7

%include Solaris.inc

Name:            SFE%{name}
Summary:         Download, build, install, upgrade, and uninstall Python packages easily
URL:             http://peak.telecommunity.com/DevCenter/setuptools
Version:         %{version}
Source0:         http://cheeseshop.python.org/packages/source/s/%{oname}/%{oname}-%{version}.tar.gz
SUNW_BaseDir:    %{_basedir}
BuildRoot:       %{_tmppath}/%{name}-%{version}-build
BuildRequires:   SUNWPython-devel

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n %oname-%version

%build
python setup.py build
perl -pi -e 's|^#!python|#!/usr/bin/python|' easy_install.py setuptools/command/easy_install.py

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix=$RPM_BUILD_ROOT/%_prefix --old-and-unmanageable

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/easy_install
%{_bindir}/easy_install-2.4
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/setuptools-%{version}-py%{pythonver}.egg-info
%{_libdir}/python%{pythonver}/vendor-packages/setuptools/*
%{_libdir}/python%{pythonver}/vendor-packages/pkg_resources.pyc
%{_libdir}/python%{pythonver}/vendor-packages/easy_install.pyc
%{_libdir}/python%{pythonver}/vendor-packages/site.pyc
%{_libdir}/python%{pythonver}/vendor-packages/pkg_resources.py
%{_libdir}/python%{pythonver}/vendor-packages/easy_install.py
%{_libdir}/python%{pythonver}/vendor-packages/site.py

%changelog
* Thu Feb 07 2008 Brian Cameron  <brian.cameron@sun.com>
- Cleanup
* Fri Oct 05 2007 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.6c7
* Tue Jul 10 2007 Brian Cameron  <brian.cameron@sun.com>
- New spec

