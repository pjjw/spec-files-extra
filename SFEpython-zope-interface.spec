#
# spec file for package SFEpython-zope-interface
#
# includes module(s): ZopeInterface
#
%define         tarname  zope.interface

%include Solaris.inc

Name:            SFEpython-zope-interface
Summary:         The zope interface module
URL:             http://pypi.python.org/pypi/zope.interface
Version:         3.4.1
Source0:         http://pypi.python.org/packages/source/z/zope.interface/zope.interface-%{version}.tar.gz
SUNW_BaseDir:    %{_basedir}
BuildRoot:       %{_tmppath}/%{name}-%{version}-build
BuildRequires:	 SUNWPython-devel

%include default-depend.inc

%define pythonver 2.4

%description
This package provides the zope Interface module.

Interfaces are objects that specify (document) the external behavior
of objects that "provide" them.  An interface specifies behavior
through: 

- Informal documentation in a doc string

- Attribute definitions

- Invariants, which are conditions that must hold for objects that
  provide the interface

Attribute definitions specify specific attributes. They define the
attribute name and provide documentation and constraints of attribute
values. Attribute definitions can take a number of forms, as we'll
see below.

%prep
%setup -q -n %{tarname}-%{version} 

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root  %buildroot

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/zope
%{_libdir}/python%{pythonver}/vendor-packages/%{tarname}-%{version}-py%{pythonver}-nspkg.pth
%{_libdir}/python%{pythonver}/vendor-packages/%{tarname}-%{version}-py%{pythonver}.egg-info

%changelog
* Thu Jan 24 2008 Darren Kenny <darren.kenny@sun.com
- Bump to 3.4.1
* Tue Jul 10 2007 Brian Cameron <brian.cameron@sun.com>
- Created spec
