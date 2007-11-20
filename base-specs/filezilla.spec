#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%define version_str 3.0.0-beta11_src
Name:		filezilla
Summary:	FileZilla FTP client
Version:	3.0.0
License:	GPL
URL:		http://filezilla.sourceforge.net/
Source:	    http://superb-east.dl.sourceforge.net/sourceforge/filezilla/FileZilla_%{version_str}.tar.bz2
Patch1:     %{name}-01-autogen.diff
Patch2:     %{name}-02-vector-begin.diff
Patch3:     %{name}-03-strrchr.diff
Patch4:     %{name}-04-socket.diff
Patch5:     %{name}-05-po-error.diff
Patch6:     %{name}-06-vector-begin-more.diff
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FileZilla is a fast and reliable FTP client and server with lots of
useful features and an intuitive interface.

%prep
%setup -q -n %{name}-3.0.0-beta11
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

./autogen.sh
./configure  --prefix=%{_prefix}     \
			--libdir=%{_libdir}     \
			--libexecdir=%{_libexecdir} \
			--datadir=%{_datadir}       \
			--mandir=%{_mandir}     \
			--sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS docs/todo.txt
%attr(755,root,root) %{_bindir}/filezilla
%attr(755,root,root) %{_bindir}/fzsftp
%dir %{_datadir}/filezilla
%{_datadir}/filezilla/resources


%changelog
* Mon Aug 06 2006 - nonsea@users.sourceforge.net
- Initial version
