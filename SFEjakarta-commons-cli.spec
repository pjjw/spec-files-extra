#
# spec file for package SFEjakarta-commons-cli
#
# includes module(s): jakarta-commons-cli
#
%include Solaris.inc

%define src_name commons-cli
%define src_ver 1.1
%define src_url http://www.apache.org/dist/jakarta/commons/cli/source

%define _javadir %{_datadir}/java
%define _javadocdir %{_datadir}/javadoc

Name:		SFEjakarta-commons-cli
Summary:	Jakarta Commons CLI - API for working with command line
Version:	%{src_ver}
License:	Apache
Group:		Development/Languages/Java
Source:		%{src_url}/%{src_name}-%{src_ver}-src.tar.gz
URL:		http://logging.apache.org/commons/cli/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package doc
Summary:                 %{summary} - Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%package javadoc
Summary:                 %{summary} - API Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}-src

%build
export JAVA_HOME=/usr/java
install -d lib
ant dist -Dnoget="true"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{src_name}-%{version}}
install -d $RPM_BUILD_ROOT%{_docdir}/%{src_name}-%{version}
install -c dist/%{src_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
(
  cd $RPM_BUILD_ROOT%{_javadir}
  ln -s %{src_name}-%{src_ver}.jar %{src_name}.jar
)
cp -r dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{src_name}-%{version}
cp dist/*.txt $RPM_BUILD_ROOT%{_docdir}/%{src_name}-%{version}

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

%files doc
%defattr(-,root,bin)
%dir %attr(755,root,sys) %{_datadir}
%dir %attr(755,root,other) %{_docdir}
%{_docdir}/*

%changelog
* Sat Sep  8 2007 - dougs@truemail.co.th
- Initial version
