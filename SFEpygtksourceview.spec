#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define python_version 2.4

Name:                SFEpygtksourceview
Summary:             Python bindings for GtkSourceView 2
Version:             1.90.4
Source:              http://ftp.gnome.org/pub/GNOME/sources/pygtksourceview/1.90/pygtksourceview-%{version}.tar.bz2
URL:                 http://www.gnome.org
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-python-libs
Requires: SUNWgnome-gtksourceview
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SUNWgnome-gtksourceview-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n pygtksourceview-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
	     %{gtk_doc_option}   \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python?.?/vendor-packages

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/pygtk
%{_datadir}/gtk-doc

%changelog
* Tue Sep 04 2007 - damien.carbery@sun.com
- Initial spec
