#
# spec file for package SFElog4j
#
# includes module(s): log4j
#
%include Solaris.inc

%define src_name log4j
%define src_ver 1.2.15
%define src_url http://www.apache.org/dist/logging/%{src_name}/%{src_ver}

%define _javadir %{_datadir}/java
%define _javadocdir %{_datadir}/javadoc

Name:		SFElogging-log4j
Summary:	log4j - logging for Java
Version:	%{src_ver}
License:	Apache
Group:		Development/Languages/Java
Source:		%{src_url}/apache-%{src_name}-%{src_ver}.tar.gz
URL:		http://logging.apache.org/log4j/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package javadoc
Summary:                 %{summary} - API Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n apache-%{src_name}-%{src_ver}

%build
export JAVA_HOME=/usr/java
ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{src_name}-%{version}}
install dist/lib/log4j-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
( cd  $RPM_BUILD_ROOT%{_javadir} && ln -s log4j-%{version}.jar log4j.jar )
cp -r docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{src_name}-%{version}

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
