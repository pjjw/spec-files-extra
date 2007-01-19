#
# spec file for package SFEphp
#
# includes module(s): php
#
%include Solaris.inc

Name:                    SFEphp
Summary:                 php - Hypertext Preprocessor - general-purpose scripting language for Web development
Version:                 5.2.0
# TODO: Get a good source url. php.net ones end with "/from/a/mirror"
Source:                  http://www.php.net/download/php-%{version}.tar.bz2
URL:                     http://www.php.net/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWapch2u
Requires: SUNWmysqlu
BuildRequires: SUNWmysqlS

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun-root


%prep
%setup -q -n php-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="%{_ldflags}"
export CFLAGS="%optflags"
./configure --prefix=%{_prefix}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
	    --libexec=%{_libexec}		\
	    --sysconfdir=%{_sysconfdir}		\
	    --with-apxs2=/usr/apache2/bin/apxs	\
	    --with-mysql=/usr/sfw
	    
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

# Create a dummy httpd.conf that apxs will populate.
mkdir -p $RPM_BUILD_ROOT/etc/apache2
echo >${RPM_BUILD_ROOT}/etc/apache2/httpd.conf
echo "LoadModule /usr/dummy.so" >>${RPM_BUILD_ROOT}/etc/apache2/httpd.conf

make install INSTALL_ROOT=$RPM_BUILD_ROOT

# Remove the dummy line and rename the file.
awk '!/dummy/ {print}' ${RPM_BUILD_ROOT}/etc/apache2/httpd.conf > ${RPM_BUILD_ROOT}/etc/apache2/httpd-php.conf
# Remove the generated files.
rm ${RPM_BUILD_ROOT}/etc/apache2/httpd.conf*

# Remove files and dirs that should probably be re-generated on the destination
# machine and not simply installed.
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/pear.conf
rm -r ${RPM_BUILD_ROOT}/.registry
rm -r ${RPM_BUILD_ROOT}/.channels
rm -r ${RPM_BUILD_ROOT}/.filemap
rm -r ${RPM_BUILD_ROOT}/.lock
rm -r ${RPM_BUILD_ROOT}/.depdblock
rm -r ${RPM_BUILD_ROOT}/.depdb

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/php
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%{_prefix}/apache2

%files root
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/apache2

%changelog
* Fri Jan 19 2007 - daymobrew@users.sourceforge.net
- Initial spec
