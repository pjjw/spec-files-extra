#
# spec file for package SFEpython-pyro
#
# includes module(s): Pyro
#
%define src_name    Pyro
%define src_url     http://superb-east.dl.sourceforge.net/sourceforge/pyro

%define python_version 2.4

%include Solaris.inc

Name:                SFEpython-pyro
Summary:             An Advanced Distributed Object Technology for Python
URL:                 http://pyro.sourceforge.net
Version:             3.7
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
Requires: SUNWPython

%prep
%setup -q -n %{src_name}-%{version}

%build
cat > setup.cfg << EOT
[bdist_rpm]
doc_files = LICENSE,docs
[install-options]
unattended=1
[install]
optimize=0
install-scripts=%{_bindir}
EOT
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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Sun Oct 07 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial spec
