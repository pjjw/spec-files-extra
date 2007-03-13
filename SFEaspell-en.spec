#
# spec file for package SFEaspell-en
#
# includes module(s): aspell-en
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
%include Solaris.inc
%use aspell = aspell-en.spec

Name:          SFEaspell-en
Summary:       A Spell Checker - English
Version:       %{aspell.version}
SUNW_BaseDir:  %{_prefix}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEaspell
BuildRequires: SFEaspell-devel

%prep
rm -rf %name-%version
mkdir -p %name-%version
%aspell.prep -d %name-%version

%build
export PATH=%{_libdir}/aspell:$PATH
export CFLAGS="%optflags"
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="%_ldflags"
%aspell.build -d %name-%version

%install
%aspell.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Tue Mar 13 2007 - jeff.cai@sun.com
- Move to sourceforge from opensolaris.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 11 2006 - halton.huo@sun.com
- Change %defattr to (-, root, other).
* Fri Apr 21 2006 - halton.huo@sun.com.
- Add %{_libdir}/aspell to PATH, 
  this is becuase aspell change, refer to LSARC/2006/231
* Fri Jan 27 2006 - damien.carbery@sun.com
- Remove share package as all files installed to _libdir.
* Thu Mar 11 2004 - <laca@sun.com>
- initial version created
