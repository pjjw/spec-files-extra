#
# spec file for package SFEgnome-menu-editor.spec
#
# includes module(s): alacarte
#
%include Solaris.inc
%define python_version 2.4

Name:                    SFEgnome-menu-editor
Summary:                 alacarte - GNOME menu editor
Version:                 0.9.90
Source:                  http://ftp.gnome.org/pub/GNOME/sources/alacarte/0.9/alacarte-%{version}.tar.bz2
Patch1:                  alacarte-01-force-reload.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SUNWPython
Requires: SUNWgnome-libs
Requires: SUNWgnome-python-libs
Requires: SUNWpostrun

%prep
%setup -q -n alacarte-%version
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export PYTHON="/usr/bin/python"

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
make -j $CPUS \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages

%install
make DESTDIR=$RPM_BUILD_ROOT install \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyc" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/gtk-update-icon-cache || exit 0';
  echo 'rm -f %{_datadir}/icons/*/icon-theme.cache' ;
  echo 'ls -d %{_datadir}/icons/* | xargs -l1 /usr/bin/gtk-update-icon-cache'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u -t 5

%files
%defattr(-, root, bin)
%{_bindir}/
%attr (-, root, bin) %{_libdir}/python*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/icons
%{_datadir}/alacarte

%changelog
* Wed Aug 16 2006 - harry.lu@sun.com
- bump up to 0.9.90 and add patch alacarte-01-force-reload.diff to make
  it work on solaris.
* Wed Jul  5 2006 - laca@sun.com
- rename to SFEgnome-menu-editor
- delete share subpkg
* Fri Apr 21 2006 - glynn.foster@sun.com
- Initial spec file
