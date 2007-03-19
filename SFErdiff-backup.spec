#
# spec file for package SFErdiff-backup
#
# includes module(s): rdiff-backup
#
%include Solaris.inc

Name:                SFErdiff-backup
Summary:             Convenient, transparent local/remote mirror, incremental backup
Version:             1.1.9
Source:              http://savannah.nongnu.org/download/rdiff-backup/rdiff-backup-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython

%prep
%setup -q -n rdiff-backup-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --prefix=%{_prefix} \
--root=$RPM_BUILD_ROOT \
--install-lib=/usr/lib/python2.4/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%dir %attr (0755, root, bin) %{_libdir}/python2.4/site-packages
%dir %attr (0755, root, bin) %{_libdir}/python2.4/site-packages/rdiff_backup
%{_libdir}/python2.4/site-packages/rdiff_backup/*.py*
%{_libdir}/python2.4/site-packages/rdiff_backup/*.so
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/rdiff-backup*.1
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/doc/rdiff-backup-1.1.9
%{_datadir}/doc/rdiff-backup-1.1.9/*

%changelog
* 
* Sat Mar 17 2007 - Eric Boutilier
- Initial spec
