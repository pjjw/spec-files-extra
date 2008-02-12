#
# spec file for package SFEjoal.spec
#
# includes module(s): joal
#
%include Solaris.inc

%define src_name	joal
%define src_url		http://download.java.net/media/joal/builds/nightly

Name:                   SFEjoal
Summary:                Java bindings for OpenAL
Version:                1.1.2-pre-20080211
Source:                 %{src_url}/%{src_name}-%{version}-src.zip
Patch1:			joal-01-solaris.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEantlr-devel
BuildRequires: SFEantlr
BuildRequires: SFEopenal-devel
Requires: SFEopenal

%prep
%setup -q -c -n %{name}-%{version}
%patch1 -p1
mkdir -p joal/make/lib/solaris-i586
mkdir -p joal/make/lib/solaris-sparc

%build
cd gluegen/make
cp gluegen.properties ../..
ant -Duser.home=../..

cd ../../joal/make
cp joal.properties ../..
ant -Duser.home=../..

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
unzip -d $RPM_BUILD_ROOT joal/build/joal-*-solaris-*.zip
mv $RPM_BUILD_ROOT/joal-*/lib/* $RPM_BUILD_ROOT%{_libdir}
rm -rf $RPM_BUILD_ROOT/joal-*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%changelog
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 1.1.2-pre-20080211
* Sun May 13 2007 - dougs@truemail.co.th
- Initial version
