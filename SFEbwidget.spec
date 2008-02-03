#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEbwidget
License:             LGPL
Summary:             A suite of megawidgets for Tk
Version:             1.8.0
URL:                 http://tcllib.sourceforge.net/
Source:              http://nchc.dl.sourceforge.net/sourceforge/tcllib/BWidget-%{version}.tar.bz2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWTk

%prep
%setup -q -n BWidget-%version

%build

%install
rm -rf $RPM_BUILD_ROOT

tf=/tmp/tcl.$$
cat << _EOF_ > $tf
puts \$tcl_version
_EOF_

tcl_version=`tclsh $tf`
rm -f $tf 

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/tk${tcl_version}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/tk${tcl_version}/BWidget
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/doc

tar cpf - * | (cd ${RPM_BUILD_ROOT}%{_libdir}/tk${tcl_version}/BWidget; tar xpf - )
mv ${RPM_BUILD_ROOT}%{_libdir}/tk${tcl_version}/BWidget/BWman ${RPM_BUILD_ROOT}%{_datadir}/doc/BWidget

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sun Feb 03 2008 - moinak.ghosh@sun.com
- Initial spec.
