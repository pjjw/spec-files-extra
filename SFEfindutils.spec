#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

# Relegating to /usr/gnu to avoid name collisions
%define _prefix %{_basedir}/gnu

Name:                SFEfindutils
Summary:             GNU find, locate, and xargs
Version:             4.2.27
Source:              http://ftp.gnu.org/pub/gnu/findutils/findutils-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -q -n findutils-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -R/usr/gnu/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --infodir=%{_datadir}/info \
	    --libexecdir=%{_libexecdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rmdir $RPM_BUILD_ROOT%{_prefix}%{_localstatedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* 
* Sun Sep 24 2006 - Eric Boutilier
- Initial spec