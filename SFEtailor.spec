#
# spec file for package SFEtailor
#
# includes module(s): Tailor
#
%include Solaris.inc

%define python_version 2.4

Name:			SFEtailor
Summary:		A tool to migrate changesets between SCMs
Version:		0.9.30
Source:			http://darcs.arstecnica.it/tailor-%{version}.tar.gz
URL:			http://progetti.arstecnica.it/tailor
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_prefix}

%include default-depend.inc

Requires: SUNWPython
BuildRequires: SUNWPython-devel

%prep
%setup -q -n tailor-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix}

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages/*

%changelog
* Sat Dec 08 2007 - trisk@acm.jhu.edu
- Initial spec

