#
# spec file for package SFEgimp-texturize
#
# includes module(s): gimp-texturize
#
%include Solaris.inc

Name:                SFEgimp-texturize
Summary:             Cross-platform development framework/toolkit
Version:             2.0
Source:              http://internap.dl.sourceforge.net/sourceforge/gimp-texturize/gimp-texturize-%{version}.tgz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-img-editor-devel
Requires: SUNWgnome-img-editor

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gimp-texturize

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="-O4"
export LDFLAGS="%_ldflags"
./configure \
    --prefix=%{_prefix}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
# FIXME
mv $RPM_BUILD_ROOT%{_libdir}/locale $RPM_BUILD_ROOT%{_datadir}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gimp/*/plug-ins/texturize
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp-texturize

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Feb 11 2007 - laca@sun.com
- Initial spec
