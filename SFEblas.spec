#
# spec file for package SFEblas.spec
#
# includes module(s): blas
#
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:                   SFEblas
Summary:                BLAS - Basic Linear Algebra Subprograms
# In fact there is no version , we give it
Version:                1.1
Source:                 ftp://ftp.netlib.org/blas/blas.tgz
#Source1:		blas.Makefile
SUNW_BaseDir:           %{_basedir}
Group:			Math
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
URL:                    http://www.netlib.org/blas/
#Patch0:                blas-01.diff

Requires: SUNWcsl
Requires: SUNWlibms

%prep
%setup -q -c -n %{name}
#%patch0 -p1

%build
cd BLAS
#CC=cc CXX=CC F77=f77 FORTRAN=f77 LOADER=f77 PLAT="" 
#export CC CXX F77 FORTRAN LOADER 
make CC=cc CXX=CC F77=f77 FORTRAN=f77 LOADER=f77 PLAT=""

%install
rm -rf $RPM_BUILD_ROOT
cd BLAS
mv blas.a libblas.a
install -d -m 0755 $RPM_BUILD_ROOT/%{_libdir}
install -m 0755 libblas.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/*

%changelog
* Wed Dec 10 2008 - dauphin@enst.fr
- Initial version
