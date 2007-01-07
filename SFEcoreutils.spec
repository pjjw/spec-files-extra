#
# spec file for package SFEcoreutils
#
# includes module(s): GNU coreutils
#

%include Solaris.inc
%include usr-gnu.inc

Name:                    SFEcoreutils
Summary:                 GNU coreutils - basic file, shell and text manipulation utilities
Version:		 6.7
Source:                  http://ftp.gnu.org/pub/gnu/coreutils/coreutils-%{version}.tar.bz2
Patch1:                  coreutils-01-gettext.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms
BuildRequires: SFEautoconf
BuildRequires: SFEautomake
Requires: SUNWpostrun

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n coreutils-%version
%patch1 -p1 -b .patch01

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PATH=/usr/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

glib-gettextize -f 
libtoolize --copy --force
aclocal -I m4
autoheader
autoconf
./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}                 \
            --infodir=%{_infodir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_std_bindir}

CONFLICTING_COMMANDS="
    :basename:cat:chgrp:chmod:chown:chroot:cksum:comm:csplit:cut:date:dd:
    :df:dirname:du:echo:env:expand:expr:factor:false:fmt:fold:groups:head:
    :hostid:hostname:id:install:join:kill:ln:logname:mkdir:mkfifo:mknod:
    :nice:nl:nohup:od:paste:pathchk:pr:printf:pwd:rm:rmdir:sleep:sort:
    :split:stty:sum:sync:tail:tee:test:touch:tr:true:tty:uname:unexpand:
    :uniq:uptime:wc:who:yes:cp:ls:mv:tsort:"

cd $RPM_BUILD_ROOT%{_bindir}
for f in *; do
    # difficult to grep for "["
    if [ "x$f" = "x["; then
	( cd $RPM_BUILD_ROOT%{_basedir}/bin; ln -s ../gnu/bin/$f . )
	continue
    fi
    # don't symlink conflicting commands to /usr/bin
    echo $CONFLICTING_COMMANDS | grep ":${f}:" > /dev/null && continue
    ( cd $RPM_BUILD_ROOT%{_basedir}/bin; ln -s ../gnu/bin/$f . )
done

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

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
  echo 'coreutils.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'coreutils.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_std_bindir}
%{_std_bindir}/*
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, sys) %{_std_datadir}
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Jan  6 2007 - laca@sun.com
- update for latest /usr/gnu proposal
- add postrun script for updating info dir
* Fri Jan 05 2007 - daymobrew@users.sourceforge.net
- Bump to 6.7.
* Tue Jun 27 2006 - laca@sun.com
- Initial spec
