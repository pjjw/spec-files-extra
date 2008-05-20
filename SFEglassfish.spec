#
# spec file for package SFEglassfish
#

#  IMPORTANT: Set your initial passwords and all here.
#             in the future there should be some 
#             configuration-recipe for your individual
#             parameters. Ideas appreciated.

#  The postinstall-script sets the JAVA_HOME=/usr/jdk/instances/jdk1.5.0


%define versionstring v2ur2
%define buildnumber b04
%define targetplatform sunos_x86
%define adminuser adminadmin
%define adminpassword changethis
%define initialdomainname domain1
%define instanceport 8080
%define smfpasswordfile smfpassword.txt
 

%include Solaris.inc
Name:                    SFEglassfish
Summary:                 GlassFish - Java Application Server 
URL:                     http://glassfish.java.net
Version:                 %{versionstring}-%{buildnumber}-%{targetplatform}
#Version:                 %{versionstring}-%{buildnumber}
Source:                  http://download.java.net/javaee5/v2ur2/promoted/SunOS_X86/glassfish-installer-%{version}.jar


SUNW_BaseDir:            %{_localstatedir}/appserver
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildRequirements:
#TODO: Requirements:

%include default-depend.inc



%prep

[ -d %_builddir/glassfish-%version ] && rm -rf %_builddir/glassfish-%version

mkdir %_builddir/glassfish-%version
cd %_builddir/glassfish-%version

echo "A" | java -Xmx256m -jar %SOURCE  -console

#TODO# below: needed??
#reset file to zero length first
echo "AS_ADMIN_ADMINPASSWORD=%{adminuser}" > %_builddir/glassfish-%version/glassfish/passfile
echo "AS_ADMIN_MASTERPASSWORD=%{adminpassword}" >> %_builddir/glassfish-%version/glassfish/passfile

%build

mkdir -p %_builddir/glassfish-%version/%{_localstatedir}/appserver

mv %_builddir/glassfish-%version/glassfish %_builddir/glassfish-%version/%{_localstatedir}/appserver/

PATH=%_builddir/glassfish-%version/%{_localstatedir}/appserver/glassfish/lib/ant/bin:$PATH
chmod a+x %_builddir/glassfish-%version/%{_localstatedir}/appserver/glassfish/lib/ant/bin/ant



%install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/var/
#cp -pr %_builddir/glassfish-%version-%{buildnumber}/var/appserver/ $RPM_BUILD_ROOT/var/
cp -pr %_builddir/glassfish-%version/var/appserver/ $RPM_BUILD_ROOT/var/

%clean
rm -rf $RPM_BUILD_ROOT


%post
(  echo 'pkgparam -v SFEglassfish'
echo 'PATH=`pkgparam SFEglassfish BASEDIR`/glassfish/lib/ant/bin:`pkgparam SFEglassfish BASEDIR`/glassfish/bin:$PATH; export PATH' ;
  echo 'cd `pkgparam SFEglassfish BASEDIR`/glassfish'
  echo 'export JAVA_HOME=/usr/jdk/instances/jdk1.5.0'
  echo 'ant -f setup.xml'
  echo 'echo "ant create-domain / setup.xml done."'
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE



%files
%defattr(-, root, bin)
#do not list dirs up and including SUNW_BaseDir (/var, /var/appserver)
%dir %attr (0755, root, bin) %{_localstatedir}/appserver/glassfish
%{_localstatedir}/appserver/glassfish/*


%changelog
* Tue May 20 2008 <cypromis (at) opensolaris.org>
- Bumped version up to v2u2
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to v2 b58
* Sun Sep 23 2007  - Thomas Wagner
- Free GlassFish (not willy) to the wild
* Sat Aug 04 2007  - Thomas Wagner
- Initial spec
