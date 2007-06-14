#
# spec file for package SFEmeld
#
# includes module(s): meld
#
%include Solaris.inc

Name:                    SFEmeld
Summary:                 Meld Diff and Merge Tool
Version:                 1.1.5.1
Source:                  http://ftp.gnome.org/pub/GNOME/sources/meld/1.1/meld-%{version}.tar.bz2
Patch1:                  meld-01-msgfmt-no-checks.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: CBEbison
BuildRequires: SUNWPython
BuildRequires: SUNWgnome-python-libs-devel
Requires: SUNWgnome-libs
Requires: SUNWgnome-python-libs

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n meld-%version
%patch1 -p1
for po in po/*.po; do
  dos2unix -ascii $po $po
done

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export PYTHON="/usr/bin/python"
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export MSGFMT="/usr/bin/msgfmt"

make prefix=%{_prefix} -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make prefix=%{_prefix} install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

# Delete unneeded scrollkeeper files.
rm -rf $RPM_BUILD_ROOT%{_prefix}/var

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update' 
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun 
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0 
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update' 
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/omf/meld/meld-C.omf
%dir %attr (0755, root, other) %{_datadir}/application-registry
%{_datadir}/application-registry/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/meld
%{_datadir}/meld/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Jun 14 2007 - damien.carbery@sun.com
- Bump to 1.1.5.1.

* Tue Nov 28 2006 - glynn.foster@sun.com
- Initial version
