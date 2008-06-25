# spec file for package SFEgroovy
#

%include Solaris.inc
%define groovy_version 1.5.6


Name:           SFEgroovy
Version:        %{groovy_version}
Release:        2
License:        See: http://groovy.codehaus.org/license.html
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Summary:        Contains the base system for executing groovy scripts.
Source:         http://dist.codehaus.org/groovy/distributions/groovy-binary-%{groovy_version}.zip
BuildArch:      noarch
BuildRequires:  SUNWunzip

%description
Groovy is an object-oriented programming language for the Java Platform as an 
alternative to the Java programming language. It can be viewed as a scripting 
language for the Java Platform, as it has features similar to those of Python, 
Ruby, Perl, and Smalltalk. In some contexts, the name JSR 241 is used as an 
alternate identifier for the Groovy language.

%prep
%setup -n groovy-%{version}
rm bin/*.bat

%build

%install
install -d $RPM_BUILD_ROOT/usr/share/groovy/lib
install -p lib/* $RPM_BUILD_ROOT/usr/share/groovy/lib

install -d $RPM_BUILD_ROOT/usr/share/groovy/conf
install -p conf/* $RPM_BUILD_ROOT/usr/share/groovy/conf

install -d $RPM_BUILD_ROOT/usr/share/groovy/embeddable
install -p embeddable/* $RPM_BUILD_ROOT/usr/share/groovy/embeddable

install -d $RPM_BUILD_ROOT/usr/bin
install -p bin/* $RPM_BUILD_ROOT/usr/bin

install -d $RPM_BUILD_ROOT/usr/share/groovy
echo "export GROOVY_HOME=/usr/share/groovy" >$RPM_BUILD_ROOT/usr/share/groovy/setgroovyenv.sh
echo "setenv GROOVY_HOME /usr/share/groovy" >$RPM_BUILD_ROOT/usr/share/groovy/setgroovyenv.csh

%clean
rm -rf "$RPM_BUILD_ROOT"

%post

%postun

%files
%defattr(-,root,root)
/usr/*

%changelog
* Mon Jun 25 2008 - rafael.alfaro@gmail.com
- Initial Spec File 

