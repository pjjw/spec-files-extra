#
# spec file for package SFEpython-wx
#
# includes module(s): wx
#
%include Solaris.inc

%define src_url         %{sf_download}/wxpython
%define src_name        wxPython

Name:                   SFEpython-wx
Summary:                Python bindings for wxWidgets
URL:                    http://www.wxpython.org/
Version:                2.8.7.1
Source:                 %{src_url}/%{src_name}-src-%{version}.tar.bz2
Patch1:                 wxpython-01-interface.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWPython
BuildRequires:          SUNWPython-devel
Requires:               SFEwxwidgets
BuildRequires:          SFEwxwidgets-devel
BuildRequires:          SFEcppunit
BuildRequires:          SFEswig

%package devel
Summary:                %{summary} - development files
SUNW_BaseDir:           %{_basedir}
%include default-depend.inc
Requires:               %{name}

%define python_version  2.4

%prep
%setup -q -n %{src_name}-src-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%cxx_optflags"
export LDFLAGS="-lCrun -lCstd"
%if %cc_is_gcc
%else
export CXX="${CXX}"
%endif
export CXXFLAGS="%cxx_optflags -norunpath -xlibmil -xlibmopt -features=tmplife"
# workaround for pycc being invoked instead of pyCC
export PYCC_CC="$CXX"

cd wxPython
python setup.py build_ext --inplace

%install
rm -rf $RPM_BUILD_ROOT
cd wxPython
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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
Thu Feb 21, 2008 - trisk@acm.jhu.edu
- Initial spec
