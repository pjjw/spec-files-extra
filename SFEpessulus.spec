#
# spec file for package SFEpessulus
#
# includes module(s): pessulus
#

%include Solaris.inc
%define pythonver 2.4

Name:                    SFEpessulus
Summary:                 Pessulus
Version:                 0.10.1
Source:                  http://ftp.gnome.org/pub/GNOME/sources/pessulus/0.10/pessulus-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SUNWPython
Requires: SUNWgnome-libs
Requires: SUNWgnome-python-libs

%prep
%setup -q -n pessulus-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags "
export RPM_OPT_FLAGS="$CFLAGS"
export PYTHON="/usr/bin/python"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export LDFLAGS="%_ldflags"
export CC="cc %optflags"

glib-gettextize -f
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyc" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%{_bindir}/pessulus
%attr (-, root, bin) %{_libdir}/python*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/pessulus.desktop
%{_datadir}/pessulus

%changelog
* Fri Jun 30 2006 - laca@sun.com
- rename to SFEpessulus
- fix up %files
- remove unnecessary env variables
* Tue Jun 26 2006 - matt.keenan@sun.com
- Initial spec file
