#
# spec file for package SFExsane
#
# includes module(s): xsane
#
%include Solaris.inc

Name:                    SFExsane
Summary:                 XSane - graphical scanning frontend
Version:                 0.991
Source:			 http://www.xsane.org/download/xsane-%{version}.tar.gz
Patch1:                  xsane-01-gettext.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEsane-backends
BuildRequires: SFEsane-backends-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n xsane-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# /usr/sfw needed for libusb
export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

aclocal -I m4
libtoolize --force
glib-gettextize --force
autoconf -f
./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info
	    		
make -j$CPUS RANLIB=/usr/ccs/bin/ranlib

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT MKINSTALLDIRS=`pwd`/mkinstalldirs
rmdir $RPM_BUILD_ROOT%{_sbindir}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/sane
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Nov  5 2006 - laca@sun.com
- Create