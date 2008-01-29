#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%include usr-gnu.inc

Name:                SFEbyacc
License:             BSD
Summary:             A portable yacc variant considered to be one of the best.
Version:             20070509
URL:                 http://invisible-island.net/byacc/byacc.html
Source:              ftp://invisible-island.net/byacc/byacc.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SUNWcsl
BuildRequires:       SUNWhea

%prep
%setup -q -n byacc-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I%{gnu_inc} -D__C99FEATURES__"
export LDFLAGS="%_ldflags %{gnu_lib_path}"

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --enable-shared=yes \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_basedir}/bin
mkdir -p $RPM_BUILD_ROOT%{_basedir}/share/man

indirb=".."
indirm="../.."
for d in `echo %{_basedir} | sed '/\// /g'`
do
	indirb="${indirb}/..
	indirm="${indirm}/..
done

(cd $RPM_BUILD_ROOT%{_basedir}/bin
    ln -s ${indirb}/%{_bindir}/yacc byacc)
(cd $RPM_BUILD_ROOT%{_basedir}/share/man
    ln -s %{indirm}/%{_mandir}/man1/yacc.1 byacc.1)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_basedir}/bin
%{_basedir}/bin/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, sys) %{_basedir}/share
%dir %attr (0755, root, bin) %{_basedir}/share/man
%{_basedir}/share/man/*

%changelog
* Tue Jan 29 2008 - moinak.ghosh@sun.com
- Initial spec.
