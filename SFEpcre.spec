# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	pcre
%define src_version	7.4
%define pkg_release	1

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	PCRE - Perl Compatible Regular Expressions
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	BSD
Source:         http://easynews.dl.sourceforge.net/sourceforge/pcre/%{src_name}-%{version}.tar.gz
Packager:     	Shivakumar GN
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build
Conflicts:      SUNWpcre

#Requires:      
#BuildRequires: 

%description 
PCRE - Perl Compatible Regular Expressions

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
./configure --prefix=%{_prefix}

#%patch0 -p 1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
make

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Install-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File permissions, ownership information. Note the difference between 
# bin(_bindir),share(_datadir) & share/applications
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, sys) %{_libdir}
%{_libdir}/*

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/man
%{_datadir}/doc
#%{_datadir}/aclocal

#%dir %attr (0755, root, other) %{_datadir}/applications
#%{_datadir}/applications/*



%changelog
* Fri Jan 11 2008 - moinak.ghosh@sun.com
- Add conflict with SUNWpcre, remove -i386 from package name
* Mon Oct 29 2007 - brian.cameron@sun.com
- Bump to 7.4 and fix Source URL.

* 2007.Aug.11 - <shivakumar dot gn at gmail dot com>
- Initial spec.
