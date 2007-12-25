#
# spec file for package SFEpython-eyed3
#
# includes module(s): eyeD3
#
%include Solaris.inc

%define src_url         http://eyed3.nicfit.net/releases
%define src_name        eyeD3

Name:                   SFEpython-eyed3
Summary:                eyeD3 - A Python module and program for processing ID3 tags
URL:                    http://eyed3.nicfit.net
Version:                0.6.14
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWPython
BuildRequires:          SUNWPython-devel

%define python_version  2.4

%prep
%setup -q -n %{src_name}-%{version}

%build
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}         \
            --datadir=%{_datadir}       \
            --mandir=%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

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
%{_libdir}/python%{python_version}/vendor-packages

%dir %attr (0755, root, sys) %{_datadir}

%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Tue Dec 25 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
