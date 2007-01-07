#
# spec file for package SFEsed
#
# includes module(s): GNU sed
#
%include Solaris.inc
%include usr-gnu.inc

Name:                SFEsed
Summary:             GNU Stream Editor
Version:             4.1.5
Source:              ftp://ftp.gnu.org/gnu/sed/sed-%{version}.tar.gz
Patch1:              sed-01-gettext.diff
Patch2:              sed-02-portability.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWpostrun

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n sed-%version
%patch1 -p1 -b .patch01
%patch2 -p1 -b .patch02

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -D_LARGEFILE64_SOURCE"
export LDFLAGS="%_ldflags"

glib-gettextize -f 
libtoolize --copy --force
aclocal -I config
autoheader
autoconf
./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --infodir=%{_infodir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'sed.info sed.info-1 sed.info-2' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'sed.info sed.info-1 sed.info-2' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Jan  6 2006 - laca@sun.com
- bump to 4.1.5
- add patches gettext.diff and portability.diff
* Tue Nov 14 2006 - Eric Boutilier
- Initial spec
