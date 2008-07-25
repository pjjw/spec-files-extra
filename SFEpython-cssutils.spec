#
# spec file for package SUNWpython-cssutils
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define name Twisted-Web2
%define tarball_version 0.9.5rc2

Name:                    SFEpython-cssutils
Summary:                 A HTTP/1.1 Server Framework
URL:                     http://code.google.com/p/cssutils/
Version:                 0.9.5
Source:                  http://cssutils.googlecode.com/files/cssutils-%{tarball_version}.zip
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n cssutils-%{tarball_version}
unzip -d cssutils-%{tarball_version}.zip %{SOURCE}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/
export PYTHONPATH=$PYTHONPATH:$RPM_BUILD_ROOT/%_prefix/lib/python%{pythonver}/site-packages

python setup.py install --prefix=$RPM_BUILD_ROOT/%_prefix

# Remove files we don't need.
#rm -fR $RPM_BUILD_ROOT/%{_libdir}/python%{pythonver}/site-packages/easy-install.pth
rm -fR $RPM_BUILD_ROOT/%{_libdir}/python%{pythonver}/site-packages/site.py
rm -fR $RPM_BUILD_ROOT/%{_libdir}/python%{pythonver}/site-packages/site.pyc

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
%{_bindir}/csscombine
%{_bindir}/cssparse
%{_bindir}/csscapture
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/cssutils*.egg
%{_libdir}/python%{pythonver}/vendor-packages/easy-install.pth

%changelog
* Fri Jul 25 2008 - brian.cameron@sun.com
- Initial version.
