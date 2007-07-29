#
# spec file for package SFEtea
#
# includes module(s): tea
#
%include Solaris.inc

%define	src_ver 17.1.1
%define	src_name tea
%define	src_url	http://nchc.dl.sourceforge.net/sourceforge/tea-editor

Name:		SFEtea
Summary:	Powerful text editor
Version:	%{src_ver}
License:	GPL v2
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		tea-01-return-null.diff
Patch2:		tea-02-pipe.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
TEA is a very small, but powerful text editor with many unique features.

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

export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lX11"
export LD_OPTIONS="-L/usr/X11/lib -R/usr/X11/lib"

glib-gettextize -f
libtoolize --copy --force
aclocal
autoconf -f
autoheader
automake -a -f
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared			\
	    --disable-debug			\
	    $nlsopt

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/tea

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
