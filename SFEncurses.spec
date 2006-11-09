#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

# Relegating to /usr/gnu to avoid name collisions with regular curses files
%define _prefix %{_basedir}/gnu

Name:                SFEncurses
Summary:             Emulation of SVR4 curses
Version:             5.5
Source:              http://ftp.gnu.org/pub/gnu/ncurses/ncurses-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n ncurses-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -R/usr/gnu/lib"

./configure --prefix=%{_prefix}  \
	    --with-shared \
            --mandir=%{_mandir}

# The following hack sets LD_LIBRARY_PATH in run_tic.sh. It's necessary
# because that script -- which is only run during make install -- fails
# to find the ncurses .so libraries when the install is being done with 
# DESTDIR set. If, for your purposes, /usr/gnu is not the ultimate destination 
# for installation of this package, you need to adjust this accordingly.

perl -i.orig -lne 'print ; if (/^test -z "\${DESTDIR}" \&\& DESTDIR/) {print q^LD_LIBRARY_PATH="$DESTDIR/usr/gnu/lib"; export LD_LIBRARY_PATH^}' misc/run_tic.sh

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1*
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*.3*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*.5*
%dir %attr (0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*.7*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_datadir}/tabset
%{_datadir}/tabset/*
%dir %attr (0755, root, other) %{_datadir}/terminfo
%{_datadir}/terminfo/*

%changelog
* 
* Wed Nov 08 2006 - Eric Boutilier
- Initial spec
