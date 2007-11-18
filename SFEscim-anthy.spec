#
# spec file for package SFEscim-anthy
#
# includes module(s): scim-anthy
#
%include Solaris.inc

%define	src_name scim-anthy
%define	src_url http://iij.dl.sourceforge.jp/scim-imengine/25404

%define SUNWgnugettext      %(/usr/bin/pkginfo -q SUNWgnu-gettext && echo 1 || echo 0) 
Name:                SFEscim-anthy
Summary:             SCIM anthy IMEngine
Version:             1.2.4
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     scim-anthy-01-ss11.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEscim-devel
Requires: SFEscim
BuildRequires: SFElibanthy-devel
Requires: SFElibanthy
%if %build_l10n
%if %SUNWgnugettext
BuildRequires: SUNWgnu-gettext-devel
Requires: SUNWgnu-gettext
%else
BuildRequires: SFEgettext-devel
Requires: SFEgettext
%endif
%endif

%package devel
Summary:                 %{summary} - development files
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

export CPPFLAGS="-I/usr/gnu/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LD_OPTIONS="-L/usr/gnu/lib -R/usr/gnu/lib"

glib-gettextize --force
aclocal
libtoolize --copy --force
automake -a -f
autoconf -f

./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --with-libintl-prefix=/usr/gnu 	\
	    --disable-static			\
	    --enable-shared			\
	    $nlsopt

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/scim

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWgnu-gettext or SFEgettext.
* Sat Jul 28 2007 - dougs@truemail.co.th
- Initial spec
