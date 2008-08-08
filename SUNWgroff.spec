#
# spec file for package SUNWgroff
#
# includes module(s): groff
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
%include Solaris.inc

Name:              SUNWgroff
License:           GPL
Summary:           GNU roff Text Formatting
Version:           1.19.2
Source:            http://ftp.gnu.org/gnu/groff/groff-%{version}.tar.gz
SUNW_BaseDir:      %{_basedir}
SUNW_Copyright:    %{name}.copyright
BuildRoot:         %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n groff-%version

%build

libtoolize --force

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I .
autoconf
autoheader
./configure     --prefix=%{_prefix}             \
                --datadir=%{_datadir}           \
                --with-appresdir=%{_prefix}/X11/lib/X11/app-defaults \
                --sysconfdir=%{_sysconfdir}
make

%install
rm -rf $RPM_BUILD_ROOT%{_prefix}
mkdir -p $RPM_BUILD_ROOT%{_prefix}
make appresdir=$RPM_BUILD_ROOT%{_prefix}/X11/lib/X11/app-defaults datadir=$RPM_BUILD_ROOT%{_datadir} prefix=$RPM_BUILD_ROOT%{_prefix} man5ext=4 man7ext=5 install
rm $RPM_BUILD_ROOT/%{_datadir}/info/dir

mkdir -p $RPM_BUILD_ROOT%{_prefix}/gnu/bin

cd $RPM_BUILD_ROOT%{_prefix}/gnu/bin
ln -s ../../bin/gdiffmk diffmk
ln -s ../../bin/geqn eqn
ln -s ../../bin/ggrn grn
ln -s ../../bin/gindxbib indxbib
ln -s ../../bin/gneqn neqn
ln -s ../../bin/gnroff nroff
ln -s ../../bin/gpic pic
ln -s ../../bin/grefer refer
ln -s ../../bin/gsoelim soelim

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/groff
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/groff/*
%{_datadir}/info/groff*
%{_datadir}/doc/groff*
%{_prefix}/X11/lib/X11/app-defaults/*
%{_libdir}/groff/*
%{_mandir}/*/*
%dir %attr (0755, root, bin) %{_prefix}/gnu
%dir %attr (0755, root, bin) %{_prefix}/gnu/bin
%defattr(0777, root, root)
%{_prefix}/gnu/bin/*
%defattr(-, root, bin)

#%if %build_l10n
#%files l10n
##%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_datadir}
###%attr (-, root, other) %{_datadir}/locale
#%{_datadir}/groff/%version/*
#%endif

%changelog
* Mon Jun 23 2008 - padraig.obriain@sun.com
- initial version
* Wed Aug 05 2007 - padraig.obriain@sun.com
- Update following review
