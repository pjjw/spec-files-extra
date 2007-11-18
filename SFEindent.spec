#
# spec file for package SFEindent
#
# includes module(s): indent
#
%include Solaris.inc
%include usr-gnu.inc

%define	src_name indent
%define	src_url	ftp://ftp.gnu.org/gnu/indent

Name:		SFEindent
Summary:	GNU C indenting program
Version:	2.2.9
License:	GPL
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:         indent-01-gcc4.diff
Patch2:         indent-02-info.diff
Patch3:         indent-03-make-jN.diff
Patch4:         indent-04-overflow.diff
Patch5:         indent-05-pl.po-update.diff
Patch6:         indent-06-po-fix.diff
Patch7:         indent-07-zh_TW.diff
Patch8:         indent-08-po-makefile.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Indent is a GNU program for beautifying C code, so that it is easier
to read. Indent can also convert from one C writing style to a
different one. Indent understands correct C syntax and tries to handle
incorrect C syntax.

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_prefix}
%include default-depend.inc
Requires: %name

%package doc
Summary:                 %{summary} - Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
# %patch7 -p1
%patch8 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
glib-gettextize --copy --force
intltoolize --copy --force --automake
aclocal
autoconf -f
automake -a -c -f
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --docdir=%{_docdir}		\
	    --disable-static		\
	    --enable-shared		\
	    $nls

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_infodir}/dir

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

[ -d $RPM_BUILD_ROOT%{_prefix}/doc ] && {
    mv $RPM_BUILD_ROOT%{_prefix}/doc $RPM_BUILD_ROOT%{_datadir}
}

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || {
    /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
}

%postun
[ ! -x /usr/sbin/fix-info-dir ] || {
    /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_prefix}/man
%{_mandir}
%dir %attr(0755, root, sys) %{_std_datadir}
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
