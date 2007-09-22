# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	astyle
%define src_version	1.18
%define pkg_release	1
%define src_tarball %{src_name}_%{src_version}__linux.tar.gz

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
Summary:      	astyle : source code indenter, formatter, and beautifier for the C, C++, C# and Java programming languages
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPLv2
Group:          Development/Tools
Source:         http://jaist.dl.sourceforge.net/sourceforge/astyle/%{src_tarball}
URL:            http://astyle.sourceforge.net
Packager:     	Shivakumar GN
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build


#Ideally these should be included for requires: glib2, gtk2, pango
#Requires:      
#BuildRequires: 

%description 
Artistic Style is a source code indenter, formatter, and beautifier for the C, C++, C# and Java programming languages.

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Packages to build
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

#%package -n SFE%{src_name}-l10n
#Summary:                 %{summary} - l10n files
#SUNW_BaseDir:            %{_basedir}
#Requires:                %{name}

#%package -n SFEgeany-docs
#Summary:                 %{summary} - documentation, man pages
#SUNW_BaseDir:            %{_basedir}
#Requires:                %{name}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{name}

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
export LDFLAGS="%_ldflags"

cd src
make -j$CPUS

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -m 755 -c ./src/astyle $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*


%changelog
* 2007.Aug.08 - <shivakumar dot gn at gmail dot com>
