#
# spec file for package SFEfreeciv.spec
#
# includes module(s): freeciv
#
%include Solaris.inc

Name:                    SFEfreeciv
Summary:                 freeciv - a multiplayer strategy game
Version:                 2.1.0-beta4
Source:                  ftp://ftp.freeciv.org/freeciv/beta/freeciv-%{version}.tar.bz2
Patch1:                  freeciv-01-signedchar.diff
Patch2:                  freeciv-02-output_type.diff
Patch3:                  freeciv-03-strlcpy.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package share
Summary:                 freeciv - platform independant files, /usr/share
SUNW_BaseDir:            %{_basedir}
Requires: %name
%include default-depend.inc

%prep
%setup -q -n freeciv-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I m4"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
            --disable-nls			\
            --enable-shared			\
	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Sounds are working, Hmmm something to fix!!!
rm -rf $RPM_BUILD_ROOT/%{datadir}freeciv/stdsounds*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%files share
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man6
%{_mandir}/man6/*
%{_datadir}/applications
%{_datadir}/freeciv
%{_datadir}/pixmaps

%changelog
* Sun Apr 21 2006 - dougs@truemail.co.th
- Bumped to 2.1.0-beta4
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
