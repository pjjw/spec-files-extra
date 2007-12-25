#
# spec file for package SFEpython-feedparser
#
# includes module(s): feedparser
#
%include Solaris.inc

Name:                    SFEpython-feedparser
Summary:                 FeedParser - A Python module for downloading and parsing syndicated feeds.
URL:                     http://feedparser.org/
Version:                 4.1
Source:                  http://feedparser.googlecode.com/files/feedparser-%{version}.zip
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

%include default-depend.inc

%define python_version  2.4

%prep
%setup -c -q -n feedparser-%{version}

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
* Tue Dec 25 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
