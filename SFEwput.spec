#
# spec file for package SFEwput
#
# includes module(s): wput
#
%include Solaris.inc

Name:                SFEwput
Summary:             File uploader with wget-like CLI interface
Version:             0.5
Source:              %{sf_download}/wput/wput-%{version}.tgz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n wput

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

perl -i.orig -lpe 'print q!#include <sys/termios.h>\n! if $. == 22' src/progress.c

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"
export LIBS="-lsocket -lnsl"

./configure --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gunzip doc/wput.1.gz
install -D doc/wput.1 $RPM_BUILD_ROOT%{_mandir}/man1/wput.1
install -D wput $RPM_BUILD_ROOT%{_bindir}/wput

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/wput
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/wput.1

%changelog
* Wed Mar 28 2007 - Eric Boutilier
- Initial spec
