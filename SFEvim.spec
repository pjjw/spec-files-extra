#
# spec file for package SFEvim.spec
#
# includes module(s): vim
#
%include Solaris.inc

%define vim_version 70

Name:         SFEvim
Summary:      Vim - vi improved
Version:      7.0
Source:       ftp://ftp.vim.org/pub/vim/unix/vim-%{version}.tar.bz2
Source1:      ftp://ftp.vim.org/pub/vim/extra/vim-%{version}-lang.tar.gz
Source2:      http://cscope.sourceforge.net/cscope_maps.vim
URL:          http://www.vim.org
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWlibms
Requires: SUNWmlib
Requires: SUNWxwrtl
Requires: SUNWTcl
Requires: SUNWPython
Requires: SFEruby
Requires: SUNWperl584core
BuildRequires: SUNWPython-devel
BuildRequires: SFEcscope
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWmlibh

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
%setup -q -D -T -b 1 -c -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -R/usr/sfw/lib"
cd vim%{vim_version}
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}	     \
            --enable-perlinterp \
            --enable-pythoninterp \
            --enable-tclinterp \
            --with-tclsh=tclsh8.3 \
            --enable-rubyinterp \
            --enable-multibyte \
            --disable-hangulinput \
            --enable-cscope \
            --enable-gui=gnome2 \
            --disable-fontset \
            --enable-netbeans

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd vim%{vim_version}
make DESTDIR=$RPM_BUILD_ROOT install
install --mode=0644 %SOURCE2 $RPM_BUILD_ROOT%{_datadir}/vim/vim%{vim_version}/plugin
rm $RPM_BUILD_ROOT%{_mandir}/man1/ex.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/view.1

rm -f $RPM_BUILD_ROOT%{_bindir}/ex
rm -f $RPM_BUILD_ROOT%{_bindir}/view

mkdir -p $RPM_BUILD_ROOT%{_prefix}/gnu/bin
cd $RPM_BUILD_ROOT%{_prefix}/gnu/bin
ln -s ../../bin/vim ex
ln -s ../../bin/vim view

find $RPM_BUILD_ROOT%{_mandir} -name view.1 -exec rm -f {} \;
find $RPM_BUILD_ROOT%{_mandir} -name ex.1 -exec rm -f {} \;

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1gnu
cd $RPM_BUILD_ROOT%{_mandir}
for d in *; do
    test $d = man1 && continue
    test -f $d/man1/vim.1 || continue
    mkdir -p $d/man1gnu && \
	cd $d/man1gnu && \
	ln -s ../man1/vim.1 view.1gnu && \
	ln -s ../man1/vim.1 ex.1gnu && \
	cd ../..
done
	

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf %{_datadir}/vim/vim%{vim_version}/lang
rm -f %{_mandir}/[a-z][a-z]
rm -f %{_mandir}/[a-z][a-z].*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_prefix}/gnu
%dir %attr (0755, root, bin) %{_prefix}/gnu/bin
%{_prefix}/gnu/bin/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vim
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/man1/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vim/vim%{vim_version}/lang
%{_mandir}/[a-z][a-z]
%{_mandir}/[a-z][a-z].*
%endif

%changelog
* Mon Jul 10 2006 - laca@sun.com
- rename to SFEvim
- bump to 7.0
- delete -share subpkg, add -l10n subpkg
- update file attributes
- enable a bunch of features, add dependencies
* Wed Jun 28 2006 - halton.huo@sun.com
- Enable cscope plugin.
* Thu Apr  6 2006 - damien.carbery@sun.com
- Update Build/Requires after check-deps.pl run.
* Fri Jan 27 2005 - glynn.foster@sun.com
- Initial version
