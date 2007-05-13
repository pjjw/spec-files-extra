#
# spec file for package SFEjogl.spec
#
# includes module(s): jogl
#
%include Solaris.inc

%define src_name	jogl
%define src_url		http://download.java.net/media/jogl/builds/nightly

Name:                   SFEjogl
Summary:                Java bindings for OpenGL - JSR-231
Version:                1.1.1-pre-20070511
Source:                 %{src_url}/%{src_name}-%{version}-src.zip
Patch1:			jogl-01-solaris.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFECg-devel
Requires: SFECg
BuildRequires: SFEantlr-devel
BuildRequires: SFEantlr

%prep
%setup -q -c -n %{name}-%{version}
%patch1 -p1
mkdir -p jogl/make/lib/solaris-i586
mkdir -p jogl/make/lib/solaris-sparc

%build
cd gluegen/make
cp gluegen.properties ../..
ant -Duser.home=../..

cd ../../jogl/make
cp jogl.properties ../..
ant -Duser.home=../.. -Djogl.cg=1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp jogl/build/jogl.jar $RPM_BUILD_ROOT%{_libdir}
cp jogl/build/obj/lib*.so* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%changelog
* Sun May 13 2007 - dougs@truemail.co.th
- Initial version
