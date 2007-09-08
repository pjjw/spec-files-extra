#
# spec file for package SFEjunit
#
# includes module(s): junit
#
%include Solaris.inc

%define src_name junit
%define src_ver 4.4
%define src_url http://dl.sourceforge.net/%{src_name}
%define src_ver1 1.1
%define src_url1 http://hamcrest.googlecode.com/files

%define _javadir %{_datadir}/java
%define _javadocdir %{_datadir}/javadoc

Name:		SFEjunit
Summary:	JUnit - regression testing framework
Version:	%{src_ver}
License:	IBM Common Public License v1.0
Group:		Development/Languages/Java
Source:		%{src_url}/%{src_name}-%{src_ver}-src.jar
Source1:	%{src_url1}/hamcrest-all-%{src_ver1}.jar
URL:		http://www.junit.org/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package javadoc
Summary:                 %{summary} - API Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}
cd %{name}-%{version}
install -d javadoc

jar fxv %{SOURCE0}
cp %{SOURCE1} .

%build
cd %{name}-%{version}
export JAVA_HOME=/usr/java
javac -classpath hamcrest-all-1.1.jar:. $(find . -name '*.java')
jar cvf %{src_name}-%{version}.jar $(find . -type f '!' -name '*.java')
javadoc -d javadoc $(find -name '*.java') || :

%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{src_name}-%{version}}
install *.jar $RPM_BUILD_ROOT%{_javadir}
(
  cd $RPM_BUILD_ROOT%{_javadir}
  ln -s %{src_name}-%{src_ver}.jar %{src_name}.jar
  ln -s hamcrest-all-%{src_ver1}.jar hamcrest.jar
)
cp -r javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{src_name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr(755,root,sys) %{_datadir}
%{_javadir}

%files javadoc
%defattr(-,root,bin)
%dir %attr(755,root,sys) %{_datadir}
%{_javadocdir}

%changelog
* Sat Sep  8 2007 - dougs@truemail.co.th
- Initial version
