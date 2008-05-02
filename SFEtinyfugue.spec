#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEtinyfugue
Summary:             Flexible, screen-oriented MUD client
Version:             5.0b8
Source:              http://surfnet.dl.sourceforge.net/sourceforge/tinyfugue/tf-50b8.tar.gz
Patch1:              tinyfugue-01-installprefix.diff
Patch2:              tinyfugue-02-remove-inline.diff	

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n tf-50b8
%patch1 -p0
%patch2 -p0

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -R/usr/sfw/lib -L%{_libdir} -R%{_libdir}"
export CPPFLAGS="-I/usr/sfw/include -I%{_includedir}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}
make install IP=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
cp src/tf.1.nroffman $RPM_BUILD_ROOT/%{_mandir}/man1/tf.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/tf-lib
%{_datadir}/tf-lib/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1

%changelog
* Tue May  2 2008 - river@wikimedia.org
- Initial spec
