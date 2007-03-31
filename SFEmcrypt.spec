#
# spec file for package SFEmcrypt
#
# includes module(s): mcrypt
#
%include Solaris.inc

Name:         SFEmcrypt
Summary:      mcrypt, replacement for Unix crypt under the GPL plus more algorithms and modes
License:      Other
Group:        System/Libraries
Version:      2.6.5
Summary:      mcrypt, libmcrypt, replacements for the old Unix crypt
Source:       http://prdownloads.sourceforge.net/mcrypt/mcrypt-%{version}.tar.bz2
#Patch1:       mcrypt-include-mglobal-01.diff
Patch2:	      mcrypt-Makefile-symlink-to-destdir-02.diff 

SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

BuildRequires: SFElibmcrypt-devel
BuildRequires: SFElibmhash-devel
Requires: SUNWzlib
Requires: SFElibmcrypt
Requires: SFElibmhash

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc               
                           

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif


%prep
%setup -q -n mcrypt-%version
#%patch1 -p1
%patch2 -p1
#autoconf

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointers"
export LDFLAGS="%_ldflags"



./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%dir %attr(755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%changelog
* Sun Mar 31 2007 - Thomas Wagner
- Initial spec
