#
# spec file for package SFEnotify-python
#
# includes module(s): notify-python
#

%include Solaris.inc
Name:                    SFEnotify-python
Summary:                 Python bindings for libnotify
URL:                     http://www.galago-project.org/
Version:                 0.1.1
Source:                  http://www.galago-project.org/files/releases/source/notify-python/notify-python-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
%include default-depend.inc

%package devel
%include default-depend.inc
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires: SUNWgnutls

%define pythonver 2.4

%prep
%setup -q -n notify-python-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

autoheader
aclocal $ACLOCAL_FLAGS
autoconf
automake -a -c -f
./configure --prefix=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/gtk-2.0/pynotify
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/pygtk

%files devel
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Apr 12 2008 - brian.cameron@sun.com
- created
