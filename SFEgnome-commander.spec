#
# spec file for package SFEgnome-commander
#
# includes module(s): gnome-commander
#
%include Solaris.inc

Name:                    SFEgnome-commander
Summary:                 Meld Diff and Merge Tool
Version:                 1.2.4
Source:                  http://ftp.gnome.org/pub/GNOME/sources/gnome-commander/1.2/gnome-commander-%{version}.tar.bz2
# owner:dcarbery type:bug bugzilla:446361
Patch1:                  gnome-commander-01-Wall.diff
# owner:dcarbery type:bug bugzilla:446361
Patch2:                  gnome-commander-02-empty-struct.diff
# owner:dcarbery type:bug bugzilla:446361
Patch3:                  gnome-commander-03-fnmatch-extension.diff
# owner:dcarbery type:bug bugzilla:365227
Patch4:                  gnome-commander-04-obsolete-mmap-opt.diff
# owner:dcarbery type:bug bugzilla:446361
Patch5:                  gnome-commander-05-void-return.diff
# owner:dcarbery type:bug bugzilla:446361
Patch6:                  gnome-commander-06-bad-ternary-code.diff
# owner:dcarbery type:bug bugzilla:446361
Patch7:                  gnome-commander-07-typedef-comma.diff
# owner:dcarbery type:bug bugzilla:446361
Patch8:                  gnome-commander-08-warnx.diff
# owner:dcarbery type:bug bugzilla:446361
Patch9:                  gnome-commander-09-other.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
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
%setup -q -n gnome-commander-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

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

aclocal $ACLOCAL_FLAGS -I m4
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}
make prefix=%{_prefix} -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

# Delete unneeded scrollkeeper files.
rm -r $RPM_BUILD_ROOT/var

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
%{_datadir}/omf/gnome-commander/gnome-commander-C.omf
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/gnome-commander.1
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Jun 12 2007 - damien.carbery@sun.com
- Add patches, 08-warnx and 09-other, to fix a few more build issues.
- Update %files and %install now that build is working.

* Mon Jun 11 2007 - damien.carbery@sun.com
- Initial version
