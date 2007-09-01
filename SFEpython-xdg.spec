#
# spec file for package SFEpython-xdg
#
# includes module(s): xdg
#
%define oname xdg
%define name python-%oname
%define version 0.15

%include Solaris.inc

Name:            SFE%{name}
Summary:         Python library to access freedesktop.org standards
URL:             http://www.freedesktop.org/wiki/Software/pyxdg
Version:         %{version}
Source0:         http://www.freedesktop.org/~lanius/py%{oname}-%{version}.tar.gz
SUNW_BaseDir:    %{_basedir}
BuildRoot:       %{_tmppath}/%{name}-%{version}-build
BuildRequires:   SUNWPython-devel

%include default-depend.inc

%define pythonver 2.4

%description
Extensions to python-distutils for large or complex distributions.

%prep
%setup -q -n py%oname-%version

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix=$RPM_BUILD_ROOT/%_prefix

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/xdg/*

%changelog
* Fri Aug 31 2007 - trisk@acm.jhu.edu
- Initial spec

