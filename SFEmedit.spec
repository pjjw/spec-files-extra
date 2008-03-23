# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	medit
%define src_version	0.9.3
%define pkg_release	1

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Preamble 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	Text editor
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPLv2
Group:          Development/Tools
Source:         %{sf_download}/mooedit/%{src_name}-%{src_version}.tar.bz2
Vendor:       	medit
URL:            http://mooedit.sourceforge.net
Packager:     	Komala, Jayanthi
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
#BuildRoot:     %{_builddir}/%{name}-root

%description 
GNU auotool

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q
CC=gcc
export CC
LDFLAGS="-L/usr/gnu/lib"
LIBS="-lintl"
export LDFLAGS LIBS

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir}


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -lintl"

make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

rm -f $RPM_BUILD_ROOT%{_datadir}/icons/*/icon-theme.cache

for f in \
  %{_datadir}/mime/XMLnamespaces \
  %{_datadir}/mime/aliases \
  %{_datadir}/mime/globs \
  %{_datadir}/mime/magic \
  %{_datadir}/mime/mime.cache \
  %{_datadir}/mime/subclasses \
  %{_datadir}/mime/text/x-copying.xml; do
    chmod +w $RPM_BUILD_ROOT$f
    rm -f $RPM_BUILD_ROOT$f
done


%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%postun
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/doc/%{name}/*
%attr (0755, root, other) %{_datadir}/icons
%{_datadir}/moo
%{_datadir}/man
%attr (0755, root, root) %{_datadir}/mime
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_basedir}/lib
%{_basedir}/include

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Mar 23 2008 - Shivakumar GN
- Bumped from V0.8.9 to V0.9.3 
* Sun Oct 14 2007 - laca@sun.com
- add l10n subpkg
- fix packaging
* Sat Aug 11 2007 - By Komala, Jayanthi
- Initial spec

