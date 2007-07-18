#
# spec file for package SFEpython-twisted
#
# includes module(s): Twisted
#
%define name Twisted

%include Solaris.inc
Name:                    SFEpython-twisted
Summary:                 Event-based framework for internet applications
URL:                     http://twistedmatrix.com/trac/
Version:                 2.5.0
Source:                  http://tmrc.mit.edu/mirror/twisted/Twisted/2.5/Twisted-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
BuildRequires:           SFEpython-zope-interface

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n Twisted-%version

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/twisted

%changelog
* Tue Jul 10 2007 - Brian Cameron  <brian.cameron@sun.com>
- Created new spec.

