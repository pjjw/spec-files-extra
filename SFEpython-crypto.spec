#
# spec file for package SFEpython-crypto
#
# includes module(s): pycrypto
#
%include Solaris.inc

%define  src_name   pycrypto

Name:                    SFEpython-crypto
Summary:                 Cryptographic library for the Python Programming Language
URL:                     http://www.amk.ca/python/code/crypto
Version:                 2.0.1
Source:                  http://www.amk.ca/files/python/crypto/pycrypto-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           SUNWPython-devel
Requires:                SUNWPython

%define python_version  2.4

%prep
%setup -q -n pycrypto-%version

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}

%changelog
* Sat Oct 06 2007 - ananth@sun.com
- Initial spec file
