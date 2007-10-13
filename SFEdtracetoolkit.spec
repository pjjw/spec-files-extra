#
# spec file for package SFEdtracetoolkit.spec
#
# includes module(s): dtracetoolkit
#

#TODO# - fix arch (need both, i386 and sparc)
#TODO# - test relocation

%include Solaris.inc

%include base.inc

%define src_name        DTraceToolkit
%define src_url         http://www.opensolaris.org/os/community/dtrace
#mirror: %define src_url        http://www.brendangregg.com/
%define demodir		%{_basedir}/demo
%define installdir	%{demodir}/dtrace


Name:                   SFEdtracetoolkit
Summary:                DTraceToolkit
Version:                0.99
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Url:			http://www.opensolaris.org/os/community/dtrace/dtracetoolkit/
SUNW_BaseDir:           %{installdir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%description
The DTraceToolkit is a collection of useful documented scripts developed by the OpenSolaris DTrace community.
This package is relocatable at install time.




%prep
%setup -q -n %{src_name}-%{version}

%build
#nothing to do

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{installdir}
cp -pr * $RPM_BUILD_ROOT/%{installdir}



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%{installdir}/*


%changelog
* Tue Oct 13 2007 - Thomas Wagner
- initial spec
