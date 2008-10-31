#
# spec file for package SFEpyyaml
#
# includes module(s): pyyaml
#

%include Solaris.inc
Name:                    SFEpyyaml
Summary:                 A YAML parser and emitter for the Python language
URL:                     http://pyyaml.org/
Version:                 3.06
Source:                  http://pyyaml.org/download/pyyaml/PyYAML-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n PyYAML-%version

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=%{buildroot}

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/yaml/*

%changelog
* Fri Oct 31 2008 - brian.cameron@sun.com
- Bump to 3.06.
* Sat Apr 12 2008 - brian.cameron@sun.com
- created with 3.05.
