#
# spec file for package SFEpython-imaging
#
# includes module(s): Imaging
#
%include Solaris.inc

Name:                    SFEpython-imaging
Summary:                 Python's own image processing library
URL:                     http://www.pythonware.com/products/pil/
Version:                 1.1.6
Release:                 1
Source:                  http://effbot.org/downloads/Imaging-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWPython-devel
BuildRequires:           SUNWzlib
BuildRequires:           SUNWjpg-devel
BuildRequires:           SUNWpng-devel
BuildRequires:           SUNWfreetype2
Requires:                SUNWPython

%include default-depend.inc

%define pythonver 2.4

%description
The Python Imaging Library (PIL) adds image processing capabilities
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%prep
%setup -n Imaging-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --skip-build --root="%{buildroot}" --prefix="%{_prefix}"

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
%{_libdir}/python%{pythonver}/vendor-packages/PIL
%{_libdir}/python%{pythonver}/vendor-packages/PIL.pth

%changelog
* Tue Jul 10 2007 Brian Cameron  <brian.cameron@sun.com>
- Created spec.
