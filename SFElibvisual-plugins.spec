#
# spec file for package SFElibvisual.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                   SFElibvisual-plugins
Summary:                Visualization plugins for the Libvisual library
Version:                0.4.0
URL:                    http://localhost.nl/~synap/libvisual-wiki/index.php/Main_Page
Source:                 http://nchc.dl.sourceforge.net/sourceforge/libvisual/libvisual-plugins-%{version}.tar.bz2

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibvisual
BuildRequires: SUNWgnome-common-devel

%prep
%setup -q -n libvisual-plugins-%{version}

%build
if [ "x`basename $CC`" != xgcc ]
then
	%error This spec file requires Gcc, set the CC and CXX env variables
fi

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes		\
	    --enable-static=no


make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/*

%defattr (-, root, other)
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Tue Jan 29 2008 - moinak.ghosh@sun.com
- Initial spec.
