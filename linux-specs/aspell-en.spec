#
# License (c) 2003 Sun Microsystems Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
Name:     	aspell6-en
Version: 	6.0
%define tarball_suffix -0
Release:        1
Vendor:		Sun Microsystems, Inc.
Distribution:	Java Desktop System
Copyright:	Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Docdir:         %{_datadir}/doc
Autoreqprov:    on
BuildArch:      noarch
Source:		ftp://ftp.gnu.org/gnu/aspell/dict/en/%{name}-%{version}%{tarball_suffix}.tar.bz2
Summary:	English dictionaries for ASpell
Group:		Applications/Text

%define aspell_version 0.50.3
Requires:	aspell >= %{aspell_version}
BuildRequires:	aspell-devel >= %{aspell_version}

%description
ASpell requires a dictionary to function properly. This package contains the set of lists that are best for general purpose spell-checkers.

%files
%defattr(-, root, root)
%{_libdir}/aspell*/*

%prep
%setup  -q -n %{name}-%{version}%{tarball_suffix}

%build
./configure

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Mar 13 2007 - jeff.cai@sun.com
- Move to sourceforge from opensolaris.
* Thu Feb 16 2006 - halton.huo@sun.com
- Bump to 6.0-0.
- Change name from aspell-en to aspell6-en.
* Tue Dec 20 2005 - damien.carbery@sun.com
- Bump to 0.51-1.
* Fri Aug 05 2005 - laca@sun.com
- simplify spec file
* Fri Jan 28 2005 - takao.fujiwara@sun.com
- Fix the wrong description by script failure.
* Mon Oct 04 2004 - dermot.mccluskey@sun.com
- Changed aspell dep. version to 0.50.3
