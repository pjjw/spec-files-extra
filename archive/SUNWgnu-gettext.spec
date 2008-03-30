#
# spec file for package SUNWgnu-gettext
#
# includes module(s): GNU gettext
#
%include Solaris.inc
%define _prefix /usr/gnu

Name:                SUNWgnu-gettext
Summary:             GNU gettext
Version:             0.16.1
Source:              ftp://ftp.gnu.org/pub/gnu/gettext/gettext-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnu-libiconv

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

export CFLAGS32="%optflags -I/usr/gnu/include"
export CFLAGS64="%optflags64 -I/usr/gnu/include"
export CXXFLAGS32="%cxx_optflags"
export CXXFLAGS64="%cxx_optflags64"

%ifarch amd64 sparcv9

export CC=${CC64:-$CC}
export CXX=${CXX64:-$CXX}
export CFLAGS="$CFLAGS64"
export CXXFLAGS="$CXXFLAGS64"

cd gettext-%{version}-64

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}/%{_arch64}	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --without-emacs			\
	    --disable-static			\
            --with-libiconv-prefix=/usr/gnu     \
            --with-included-gettext             \
	    --enable-nls

make -j$CPUS
cd ..
%endif

cd gettext-%{version}

export CC=${CC32:-$CC}
export CXX=${CXX32:-$CXX}
export CFLAGS="$CFLAGS32"
export CXXFLAGS="$CXXFLAGS32"

./configure --prefix=%{_prefix}		\
            --libdir=%{_libdir}		\
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --without-emacs		\
	    --disable-static		\
            --with-libiconv-prefix=/usr/gnu     \
            --with-included-gettext     \
	    --enable-nls

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd gettext-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/charset.alias
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

rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

mkdir -p $RPM_BUILD_ROOT%{_basedir}/lib
cd $RPM_BUILD_ROOT%{_basedir}/lib
ln -s ../gnu/lib/libintl.so libgnuintl.so

%ifarch amd64 sparcv9
mkdir -p %{_arch64}
cd %{_arch64}
ln -s ../../gnu/lib/%{_arch64}/libintl.so libgnuintl.so
%endif

mkdir -p $RPM_BUILD_ROOT%{_basedir}/share/aclocal
mv $RPM_BUILD_ROOT%{_datadir}/aclocal/* $RPM_BUILD_ROOT%{_basedir}/share/aclocal
rmdir $RPM_BUILD_ROOT%{_datadir}/aclocal
cd $RPM_BUILD_ROOT%{_datadir}

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
%dir %attr (0755, root, bin) %{_basedir}/lib
%{_basedir}/lib/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gettext
%{_datadir}/gettext/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*.3
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/gettext
%{_libdir}/%{_arch64}/gettext/*
%endif
%defattr (-, root, other)
%{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_basedir}/share
%dir %attr (0755, root, other) %{_basedir}/share/aclocal
%{_basedir}/share/aclocal/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Sep 28 2007 - laca@sun.com
- fix %install and %files
* Fri Apr 20 2007 - Doug Scott <dougs@truemail.co.th>
- Fixed %{_datadir}/doc group
* Fri Apr 20 2007 - Doug Scott <dougs@truemail.co.th>
- Removed gettext.info autosprintf.info - conflicts with SUNWgnome-common-devel
- Removed charset.alias - conficts with SFEcoreutils
* Sun Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- Initial spec
