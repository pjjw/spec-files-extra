#
# spec file for package SFEmatplotlib
#
# includes module(s): matplotlib
#
%include Solaris.inc

%define src_url         http://%{sf_download}/matplotlib
%define src_name        matplotlib

Name:                   SFEmatplotlib
Summary:                A plotting library for Python which uses syntax similar to MATLAB
URL:                    http://matplotlib.sourceforge.net
Version:                0.91.2
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWPython
BuildRequires:          SUNWPython-devel
Requires:               SFEpython-numpy


%define python_version  2.4

%prep
%setup -q -n %{src_name}-%{version}

if [ "x`basename $CC`" != xgcc ]; then
	echo This spec file requires Gcc, set the CC and CXX env variables
	exit 1
fi

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

%changelog
* Tue Feb 11 2008 - Pradhap < pradhap (at) gmail.com >
- Fixed links
* Sun Feb 10 2008 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
