#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:           SFEanjuta
Version:        2.1.2
Summary:        GNOME IDE for C and C++
Group:          Development/Tools
License:        GPL
URL:            http://anjuta.org/
Source:         http://download.gnome.org/sources/anjuta/2.1/anjuta-%{version}.tar.bz2
# date:2007-03-28 bugzilla:423682 owner:nonsea type:bug
Patch1:         anjuta-01-suncc-zero-struct-array.diff
# date:2007-03-28 bugzilla:423727 owner:nonsea type:bug
Patch2:         anjuta-02-suncc-inline.diff
# date:2007-03-28 bugzilla:423730 owner:nonsea type:bug
Patch3:         anjuta-03-wrong-define.diff
# date:2007-03-28 bugzilla:423733 owner:nonsea type:bug
Patch4:         anjuta-04-lack-headers.diff
# date:2007-03-28 bugzilla:423737 owner:nonsea type:bug
Patch5:         anjuta-05-remove-lutil.diff
# date:2007-03-28 bugzilla:423680 owner:nonsea type:bug
Patch6:         anjuta-06-suncc-union.diff
# date:2007-03-28 bugzilla:423768 owner:nonsea type:bug
Patch7:         anjuta-07-wrong-return.diff
# date:2007-03-28 bugzilla:423772 owner:nonsea type:bug
Patch8:         anjuta-08-invalid-cast.diff
# date:2007-04-04 bugzilla:425850 owner:nonsea type:bug
Patch9:         anjuta-09-share-glue.diff
# date:2007-04-04 owner:nonsea type:branding
Patch10:         anjuta-10-solaris-grep.diff
# date:2007-04-06 bugzilla:426701 owner:nonsea type:bug
Patch11:         anjuta-11-solaris-svn.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWbash
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-devhelp
Requires: SUNWgnome-gtksourceview
Requires: SUNWgnome-libs
Requires: SUNWgnome-print
Requires: SUNWgnome-terminal
Requires: SUNWgnome-ui-designer
Requires: SUNWgnome-vfs
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWlxsl
Requires: SUNWperl584core
Requires: SUNWpcre
Requires: SUNWapch2u
Requires: SUNWneon
Requires: SFEgdl
Requires: SFEgnome-build
Requires: SFEgraphviz
Requires: SFEautogen
Requires: SUNWsvn
BuildRequires: SUNWpcre-devel
BuildRequires: SFEgdl-devel
BuildRequires: SFEgnome-build-devel
BuildRequires: SFEgraphviz-devel
BuildRequires: SFEautogen-devel


%description
Anjuta is a versatile Integrated Development Environment (IDE) for C and C++.
It has been written for GTK/GNOME, and features a number of advanced
programming facilities. It is basically a GUI interface for the collection
of command line programming utilities and tools available for the GNU system.
These are usually run via a text console, and can be unfriendly to use.

This package includes anjuta_create_global_tags.sh, which will allow you to
create an up to date, local system.tags.

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n anjuta-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

glib-gettextize -f
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}						\
            --mandir=%{_mandir}						\
	    --libdir=%{_libdir}						\
	    --includedir=%{_includedir}					\
            --sysconfdir=%{_sysconfdir}					\
	    --with-svn-include=%{_includedir}/svn			\
	    --with-svn-lib=%{_libdir}/svn				\
            --with-apr-config=%{_prefix}/apache2/bin/apr-1-config	\
            --disable-scrollkeeper

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# generated in the postinstall scripts (update-mime-database)
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS
( touch %{_datadir}/icons/hicolor || :
  touch %{_datadir}/icons/gnome || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/gnome || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS
( touch %{_datadir}/icons/hicolor  || :
  touch %{_datadir}/icons/gnome || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/gnome || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/anjuta
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/anjuta
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/anjuta*
%{_datadir}/omf/anjuta*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/anjuta*

%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/gnome
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*.png
%dir %attr (-, root, other) %{_datadir}/icons/gnome/48x48
%dir %attr (-, root, other) %{_datadir}/icons/gnome/48x48/mimetypes
%{_datadir}/icons/gnome/48x48/mimetypes/*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%dir %attr (-, root, other) %{_datadir}/icons/gnome/scalable
%dir %attr (-, root, other) %{_datadir}/icons/gnome/scalable/mimetypes
%{_datadir}/icons/gnome/scalable/mimetypes/*.svg
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/omf/anjuta/anjuta-[a-z][a-z].omf
%{_datadir}/omf/anjuta/anjuta-[a-z][a-z]_[A-Z][A-Z].omf
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/anjuta/[a-z][a-z]
%{_datadir}/gnome/help/anjuta/[a-z][a-z]_[A-Z][A-Z]
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Sat Apr 20 2007 - dougs@truemail.co.th
- Added Required: SUNWsvn, and modified patch solaris-11-svn.diff
* Fri Apr 06 2007 - nonsea@users.sourceforge.net
  Enable subversion support:
- Add require SUNWapch2u and SUNWneon.
- Add patch solaris-svn.diff.
- Add --with-svn-include --with-svn-lib --with-apr-config
  for ./configure.
* Wed Apr 04 2007 - nonsea@users.sourceforge.net
- Add patch solaris-grep.diff for using /usr/xpg4/bin/grep 
  instead /usr/bin/grep for -e option.
* Wed Apr 04 2007 - nonsea@users.sourceforge.net
- Add patch share-glue.diff.
* Thu Mar 28 2007 - nonsea@users.sourceforge.net
- Bump to 2.1.2
- Remove patch upstreamed anjuta-01-wall.diff and reorder.
* Thu Mar 28 2007 - nonsea@users.sourceforge.net
- Reorganize patches
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Initial spec
