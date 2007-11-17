#
# spec file for package SFEphp
#
# includes module(s): php
#
%include Solaris.inc

%define SUNWgnugettext      %(/usr/bin/pkginfo -q SUNWgnu-gettext && echo 1 || echo 0)

Name:                    SFEphp
Summary:                 php - Hypertext Preprocessor - general-purpose scripting language for Web development
Version:                 5.2.5
Source:                  http://www.php.net/distributions/php-%{version}.tar.bz2
URL:                     http://www.php.net/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWapch2u
%if %SUNWgnugettext
BuildRequires: SUNWgnu-gettext-devel
Requires: SUNWgnu-gettext
%else
BuildRequires: SFEgettext-devel
Requires: SFEgettext
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun-root


%prep
%setup -q -c -n php-%version
cp -pr php-%version php-%{version}-fastcgi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="%{_ldflags}"
export CFLAGS="%optflags"

cd php-%{version}-fastcgi
./configure --prefix=%{_prefix}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
	    --libexec=%{_libexec}		\
	    --sysconfdir=%{_sysconfdir}		\
         --enable-fastcgi                    \
	    --with-bz2                          \
	    --with-zlib                         \
	    --enable-mbstring                   \
	    --with-gettext=/usr/gnu             \
	    --with-pgsql=/usr

make -j$CPUS
cd ..

cd php-%version
./configure --prefix=%{_prefix}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
	    --libexec=%{_libexec}		\
	    --sysconfdir=%{_sysconfdir}		\
	    --with-bz2                          \
	    --with-zlib                         \
	    --enable-mbstring                   \
	    --with-gettext=/usr/gnu             \
	    --with-pgsql=/usr                   \
	    --with-apxs2=/usr/apache2/bin/apxs	

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

# Create a dummy httpd.conf that apxs will populate.
mkdir -p $RPM_BUILD_ROOT/etc/apache2
echo >${RPM_BUILD_ROOT}/etc/apache2/httpd.conf
echo "LoadModule /usr/dummy.so" >>${RPM_BUILD_ROOT}/etc/apache2/httpd.conf

cd php-%version
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# Copy FastCGI binary
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp ../php-%{version}-fastcgi/sapi/cgi/php $RPM_BUILD_ROOT%{_bindir}/php-cgi

cp php.ini-recommended $RPM_BUILD_ROOT%{_libdir}/php.ini

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
%{_libdir}/php.ini
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
* Sat Nov 17 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWgnu-gettext or SFEgettext.
* Sat May 5 2007 - Thomas Wagner
- Bump: to 5.2.2 (mainly security fixes)
* Wed Mar 28 2007 - Eric Boutilier
- add --enable-mbstring and --with-gettext=/usr/gnu
* Mon Mar 26 2007 - Eric Boutilier
- Work-around: Remove MySQL dependencies and --with-mysql
- Add: --with-pgsql=/usr --with-bz2 --with-zlibs 
- Add: cp php.ini-recommended $RPM_BUILD_ROOT%{_libdir}/php.ini
- Bump: to 5.2.1
* Fri Jan 19 2007 - daymobrew@users.sourceforge.net
- Initial spec
