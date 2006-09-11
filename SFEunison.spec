#
# spec file for package SFEunison
#
# includes module(s): unison
#

%include Solaris.inc
Name:                    SFEunison
Summary:                 unison - file synchronization tool
Version:                 2.17.1
Source:                  http://www.cis.upenn.edu/~bcpierce/unison/download/releases/beta/unison-%{version}.tar.gz
Patch1:                  unison-01-port-sol.diff
Patch2:                  unison-02-remote-shell.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFEocaml
BuildRequires: SFElablgtk

%prep
%setup -q -n unison-%version
%patch1 -p0
%patch2 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS=""
export LDFLAGS=""

#FIXME: make -i$CPUS fail on multiple cpus machines
#make -j$CPUS UISTYLE=text
make UISTYLE=text
mv unison unison-%{version}
#make -j$CPUS UISTYLE=gtk2
make UISTYLE=gtk2
mv unison unisongui
mv unison-%{version} unison

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp unison $RPM_BUILD_ROOT%{_bindir}
cp unisongui $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Thu Aug 24 2006 - halton.huo@sun.com
- Rename patch1, add new patch patches/unison-02-remote-shell.diff.
* Thu Jul 27 2006 - halton.huo@sun.com
- Change SFEocaml and SFElablgtk to BuildRequires.
- Correct make fail on multiple machines, need fix it later.
* Sat Jul 15 2006 - laca@sun.com
- split ocaml and lablgtk into their own pkgs
- simplify build
* Tue May 30 2006 - halton.huo@sun.com
- Add patch unison-01.diff.
* Mon May 29 2006 - halton.huo@sun.com
- Initial spec file
