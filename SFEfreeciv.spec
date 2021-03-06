#
# spec file for package SFEfreeciv.spec
#
# includes module(s): freeciv
#
%include Solaris.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

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
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
BuildRequires:	SFEsdl-mixer-devel
Requires:	SFEsdl-mixer

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/freeciv
%defattr (-, root, other)
%{_datadir}/applications
%{_datadir}/pixmaps

%changelog
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Sun Apr 21 2006 - dougs@truemail.co.th
- Added SFEsdl-mixer and enabled sound
- A slight tidy up of spec file
* Sun Apr 21 2006 - dougs@truemail.co.th
- Bumped to 2.1.0-beta4
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
