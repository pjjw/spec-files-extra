#
# spec file for package SFEemacs
#
# includes module(s): GNU emacs
#
%include Solaris.inc

Name:                    SFEemacs
Summary:                 GNU Emacs - an operating system in a text editor
Version:                 21.4
%define emacs_version    21.4a
Source:                  ftp://ftp.gnu.org/pub/gnu/emacs/emacs-%{emacs_version}.tar.gz
URL:                     http://www.gnu.org/software/emacs/emacs.html
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWxwrtl
Requires: SUNWxwplt
Requires: SUNWxwice
Requires: SUNWTiff
Requires: SUNWpng
Requires: SUNWjpg
Requires: SUNWlibms
Requires: SUNWzlib
Requires: SUNWperl584core
Requires: SUNWtexi
Requires: SUNWpostrun

%prep
%setup -q -n emacs-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CPP="/usr/sfw/bin/gcc -E"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
export PERL=/usr/perl5/bin/perl

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --infodir=%{_infodir}            \
            --sysconfdir=%{_sysconfdir} --enable-python

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	libexecdir=$RPM_BUILD_ROOT%{_libexecdir} \
        infodir=$RPM_BUILD_ROOT%{_infodir}

rm -f $RPM_BUILD_ROOT%{_bindir}/ctags
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/ctags.1
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'ada-mode autotype ccmode cl dired-x ebrowse ediff efaq emacs' ;
  echo 'emacs-mime eshell eudc forms gnus idlwave info message mh-e' ;
  echo 'pcl-cvs reftex sc speedbar vip viper widget woman' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'ada-mode autotype ccmode cl dired-x ebrowse ediff efaq emacs' ;
  echo 'emacs-mime eshell eudc forms gnus idlwave info message mh-e' ;
  echo 'pcl-cvs reftex sc speedbar vip viper widget woman' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, root)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, root) %{_datadir}/emacs
%{_datadir}/emacs/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%attr (0755, root, bin) %{_infodir}

%changelog
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEemacs
- add missing deps
* Wed Oct 12 2005 - laca@sun.com
- create
