#
# spec file for package SFEpychm
#
# includes module(s): pychm
#
%include Solaris.inc

%define	src_name pychm
%define	src_url	http://nchc.dl.sourceforge.net/sourceforge/gnochm

Name:                SFEpychm
Summary:             Python CHM module
Version:             0.8.4
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     pychm-01-inline.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEchmlib

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
env CFLAGS="%{optflags}" python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%files
%defattr (-, root, bin)
%{_libdir}

%changelog
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
