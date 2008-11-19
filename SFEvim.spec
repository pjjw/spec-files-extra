#
# spec file for package SFEvim.spec
#
# includes module(s): vim
#
%include Solaris.inc

%define vim_version 72
%define SPROsslnk      %(/usr/bin/pkginfo -q SPROsslnk && echo 1 || echo 0)

Name:         SFEvim
Summary:      Vim - vi improved
Version:      7.2
Release:      042
Source:       ftp://ftp.vim.org/pub/vim/unix/vim-%{version}.tar.bz2
Source1:      ftp://ftp.vim.org/pub/vim/extra/vim-%{version}-lang.tar.gz
Source2:      ftp://ftp.vim.org/pub/vim/extra/vim-%{version}-extra.tar.gz
Source3:      http://cscope.sourceforge.net/cscope_maps.vim
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
#Requires: SFEruby
Requires: SUNWperl584core
BuildRequires: SUNWPython-devel
# See ChangeLog for the following:
#%if %SPROsslnk
#BuildRequires: SPROsslnk
#%else
#BuildRequires: SFEcscope
#%endif
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWmlibh
BuildRequires: SUNWxwinc

# Patches 001 < 999 are patches from the base maintainer.
# If you're as lazy as me, generate the list using
# for i in `seq 1 42`; do printf "Patch%03d: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.%03d\n" $i $i; done
# And don't forget to fetch them :)
# for i in `seq 1 42`; do printf "ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.%03d\n" $i; done | wget -P $HOME/packages/SOURCES --input-file=-
Patch001: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.001
Patch002: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.002
Patch003: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.003
Patch004: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.004
Patch005: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.005
Patch006: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.006
Patch007: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.007
Patch008: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.008
Patch009: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.009
Patch010: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.010
Patch011: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.011
Patch012: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.012
Patch013: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.013
Patch014: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.014
Patch015: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.015
Patch016: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.016
Patch017: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.017
Patch018: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.018
Patch019: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.019
Patch020: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.020
Patch021: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.021
Patch022: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.022
Patch023: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.023
Patch024: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.024
Patch025: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.025
Patch026: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.026
Patch027: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.027
Patch028: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.028
Patch029: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.029
Patch030: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.030
Patch031: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.031
Patch032: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.032
Patch033: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.033
Patch034: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.034
Patch035: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.035
Patch036: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.036
Patch037: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.037
Patch038: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.038
Patch039: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.039
Patch040: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.040
Patch041: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.041
Patch042: ftp://ftp.vim.org/pub/vim/patches/7.2/7.2.042

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
%setup -q -D -T -b 2 -c -n %name-%version

# Base patches...
# for i in `seq 1 42`; do printf "%%patch%03d -p0 \n" $i; done
# Undefine _patch_options, because with the default of --fuzz=0 --unified,
# the patches fail to apply.
%define _patch_options 
cd vim%{vim_version}
%patch001 -p0 
%patch002 -p0 
%patch003 -p0 
%patch004 -p0 
%patch005 -p0 
%patch006 -p0 
%patch007 -p0 
%patch008 -p0 
%patch009 -p0 
%patch010 -p0 
%patch011 -p0 
%patch012 -p0 
%patch013 -p0 
%patch014 -p0 
%patch015 -p0 
%patch016 -p0 
%patch017 -p0 
%patch018 -p0 
%patch019 -p0 
%patch020 -p0 
%patch021 -p0 
%patch022 -p0 
%patch023 -p0 
%patch024 -p0 
%patch025 -p0 
%patch026 -p0 
%patch027 -p0 
%patch028 -p0 
%patch029 -p0 
%patch030 -p0 
%patch031 -p0 
%patch032 -p0 
%patch033 -p0 
%patch034 -p0 
%patch035 -p0 
%patch036 -p0 
%patch037 -p0 
%patch038 -p0 
%patch039 -p0 
%patch040 -p0 
%patch041 -p0 
%patch042 -p0 

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
            --with-tclsh=/usr/bin/tclsh8.4 \
            --enable-rubyinterp \
            --enable-multibyte \
            --disable-hangulinput \
            --enable-cscope \
            --enable-gui=gnome2 \
            --disable-fontset \
            --enable-netbeans \
            --with-compiledby="`id -un`" \
            --with-features=huge

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd vim%{vim_version}
make DESTDIR=$RPM_BUILD_ROOT install
install --mode=0644 %SOURCE3 $RPM_BUILD_ROOT%{_datadir}/vim/vim%{vim_version}/plugin
rm $RPM_BUILD_ROOT%{_mandir}/man1/ex.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/view.1

rm -f $RPM_BUILD_ROOT%{_bindir}/ex
rm -f $RPM_BUILD_ROOT%{_bindir}/view
ln -s vim gvim

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
rm -rf $RPM_BUILD_ROOT%{_datadir}/vim/vim%{vim_version}/lang
rm -rf $RPM_BUILD_ROOT%{_mandir}/[a-z][a-z]
rm -rf $RPM_BUILD_ROOT%{_mandir}/[a-z][a-z].*
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
* Tue Nov 19 2008 - alexander@skwar.name
- Bump to 7.2, and apply the 42 patches that are there in 
  ftp://ftp.vim.org/pub/vim/patches/7.2
- Use vim-7.2-extra
- Set tclsh to tclsh8.4
- Add compiledby information
- Add build dependency on SUNWxwinc, as without that, GUI won't be built
- Comment out Build dependency on SFEcscope or SPROsslnk; it's provided
  by pkg sunstudioexpress - and it's not a *BUILD* dependency to begin with.
- Build a binary with "huge" features (and not just "normal")
* Tue Jul 17 2007 - halton.huo@sun.com
- Bump to 7.1
* Fri Jul 13 2007 - dougs@truemail.co.th
- Fixed cscope requirement clash
* Mon Sep 11 2006 - halton.huo@sun.com
- Correct remove l10n files part
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
