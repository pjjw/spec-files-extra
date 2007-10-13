#
# spec file for package SFEpython-psyco
#
# includes module(s): pysco
#
%include Solaris.inc

%define src_url         http://internap.dl.sourceforge.net/sourceforge/psyco
%define src_name        psyco

Name:                   SFEpython-psyco
Summary:                A extension module which can massively speed up the execution of any Python code
URL:                    http://psyco.sourceforge.net
Version:                1.5.2
Source:                 %{src_url}/%{src_name}-%{version}-src.tar.gz
Patch1:                 psyco-01-inline.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWPython
BuildRequires:          SUNWPython-devel

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
%{_libdir}/python%{python_version}/vendor-packages/psyco

%changelog
* Sun Oct 14 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
