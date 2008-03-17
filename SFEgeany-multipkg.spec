# =========================================================================== 
#                    Spec File for Geany
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	geany
%define src_version	0.13
%define pkg_release	1

# %{_topdir} is by default set to RPM_BUILD_ROOT
# Default path for RPM_BUILD_ROOT is /var/tmp/pkgbuild-{username}
# Install the software here as part of package building steps

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	Geany - Light weight text editor/IDE
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPLv2
Group:          Development/Tools
Source:         http://files.uvena.de/geany/%{src_name}-%{version}.tar.bz2
Vendor:       	Enrico Troger,Nick Treleaven,Frank Lanitz
URL:            http://geany.uvena.de/
Packager:     	Shivakumar GN
BuildRoot:	%{_tmppath}/%{src_name}-%{version}-build

#Ideally these should be included for requires: glib2, gtk2, pango
#Requires:      
#BuildRequires: 

%description 
Geany is a small and fast editor with basic features of an integrated development environment.

Some features:
- syntax highlighting
- code completion
- code folding
- call tips
- folding
- many supported filetypes like C, Java, PHP, HTML, Python, Perl, Pascal
- symbol lists

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Packages to build
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

%package -n SFEgeany-l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
#Requires:                %{name}

%package -n SFEgeany-docs
Summary:                 %{summary} - documentation, man pages
SUNW_BaseDir:            %{_basedir}
#Requires:                %{name}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
CC=gcc
CXX=g++
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/gnu/lib
./configure --prefix=%{_prefix}


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/gnu/lib
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -lintl"

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}/%{src_name}
%{_libdir}/%{src_name}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/applications
%{_datadir}/geany
%{_datadir}/pixmaps
%{_datadir}/icons

%files -n SFEgeany-l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%files -n SFEgeany-docs
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/doc
%{_datadir}/man


%changelog
* 2008.Mar.17 - <shivakumar dot gn at gmail dot com>
- Bumped to V0.13
- Compile with gcc since that works out of the box
* 2007.Aug.08 - <shivakumar dot gn at gmail dot com>
- Use of %package & %files for sub-package creation
  (base pkg, doc pkg, l10n pkg)
- Introduction of custom compile/link flags
- Make uses multiple CPU systems for parallelism
* 2007.Aug.08 - <shivakumar dot gn at gmail dot com>
- Use of include files for common definitions
* 2007.Aug.07 - <shivakumar dot gn at gmail dot com>
- Initial spec. Example for a badly designed but working spec
