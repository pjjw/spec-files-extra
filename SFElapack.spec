#
# spec file for package SFElapack.spec
#
# includes module(s): lapack
#
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:                   SFElapack
Summary:                LAPACK - Linear Algebra PACKage
Version:                3.1.1
Source:                 ftp://ftp.netlib.org/lapack/lapack-%{version}.tgz
SUNW_BaseDir:           %{_basedir}
Group:			Math
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
URL:                    http://www.netlib.org/lapack/
#Patch0:                lapack-01.diff

Requires: SUNWcsl
Requires: SUNWlibms
Requires: SFEblas

%prep
%setup -q -c -n %{name}
#%patch0 -p1

%build
cd lapack-%{version}
#CC=cc CXX=CC F77=f77 FORTRAN=f77 LOADER=f77 PLAT="" 
#export CC CXX F77 FORTRAN LOADER 
mv make.inc.example make.inc
ln -s %{_libdir}/libblas.a blas.a
make CC=cc CXX=CC F77=f77 FORTRAN=f77 LOADER=f77 PLAT="" OPTS=-O3

%install
rm -rf $RPM_BUILD_ROOT
cd lapack-%{version}
mv lapack.a liblapack.a
install -d -m 0755 $RPM_BUILD_ROOT/%{_libdir}
install -m 0755 liblapack.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/*

%changelog
* Wed Dec 10 2008 - dauphin@enst.fr
- Initial version
