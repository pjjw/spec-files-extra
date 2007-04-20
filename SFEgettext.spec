#
# spec file for package SFEgettext
#
# includes module(s): GNU gettext
#
%include Solaris.inc
%include usr-gnu.inc

Name:                SFEgettext
Summary:             GNU gettext
Version:             0.16.1
Source:              ftp://ftp.gnu.org/pub/gnu/gettext/gettext-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWpostrun

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
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
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -pr gettext-%{version} gettext-%{version}-64
%endif

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

export CFLAGS32="%optflags"
export CFLAGS64="%optflags64"
export CXXFLAGS32="%cxx_optflags"
export CXXFLAGS64="%cxx_optflags64"
export LDFLAGS32="%_ldflags"
export LDFLAGS64="%_ldflags"

%ifarch amd64 sparcv9

CC -V 2>&1 | /usr/xpg4/bin/grep -q "CC: Sun C++ 5.8 Patch 121018-0[0-8]" && {
    echo "The version of the compiler you are using is known to crash the"
    echo "system when compiling this code. Please install the latest patches"
    echo "for the compiler and try again." 
    exit 1
}

export CC=${CC64:-$CC}
export CXX=${CXX64:-$CXX}
export CFLAGS="$CFLAGS64"
export CXXFLAGS="$CXXFLAGS64"
export LDFLAGS="$LDFLAGS64"

cd gettext-%{version}-64

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}/%{_arch64}	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --without-emacs			\
	    --disable-static			\
	    $nlsopt

make -j$CPUS
cd ..
%endif

cd gettext-%{version}

export CC=${CC32:-$CC}
export CXX=${CXX32:-$CXX}
export CFLAGS="$CFLAGS32"
export CXXFLAGS="$CXXFLAGS32"
export LDFLAGS="$LDFLAGS32"

./configure --prefix=%{_prefix}		\
            --libdir=%{_libdir}		\
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --without-emacs		\
	    --disable-static		\
	    $nlsopt

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd gettext-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la
cd ..
%endif


cd gettext-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

rm -rf $RPM_BUILD_ROOT%{_infodir}
rm $RPM_BUILD_ROOT%{_libdir}/charset.alias

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/gettext
%{_libdir}/gettext/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gettext
%{_datadir}/gettext/*
%dir %attr (0755, root, bin) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*.3
%dir %attr(0755, root, sys) %{_std_datadir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%config %{_libdir}/%{_arch64}/charset.alias
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/gettext
%{_libdir}/%{_arch64}/gettext/*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Apr 20 2007 - Doug Scott <dougs@truemail.co.th>
- Removed gettext.info autosprintf.info - conflicts with SUNWgnome-common-devel
- Removed charset.alias - conficts with SFEcoreutils
* Sun Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- Initial spec
