#
# spec file for package SFEpython-gsl
#
# includes module(s): pygsl
#
%include Solaris.inc

%define src_url         http://superb-east.dl.sourceforge.net/sourceforge/pygsl
%define src_name        pygsl

Name:                   SFEpython-gsl
Summary:                Python interface to GNU Scientific library
URL:                    http://pygsl.sourceforge.net
Patch1:                 pygsl-01-macro.diff
Version:                0.9.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWPython
BuildRequires:          SUNWPython-devel
Requires:               SFEgsl
BuildRequires:          SFEgsl-devel
Requires:               SFEpython-numpy

%package devel
Summary:                %{summary} - development files
SUNW_BaseDir:           %{_basedir}
%include default-depend.inc
Requires:               %{name}

%define python_version  2.4

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

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
%{_libdir}/python%{python_version}/vendor-packages

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Nov 04 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
