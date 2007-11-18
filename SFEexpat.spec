#
# spec file for package SFEexpat
#
# includes module(s): expat
#
#

%include Solaris.inc

%ifarch sparcv9 amd64
%include arch64.inc
%use expat64 = expat.spec
%endif

%include base.inc
%use expat = expat.spec

#Name:          SUNWlexpt
Name:         SFEexpat
Summary:       %{expat.summary}
Version:       %{expat.version}
# to match the SFW package:
SUNW_BaseDir:  /
BuildConflicts: SUNWlexpt
Requires: SUNWlibms

%prep
rm -rf %name-%version
mkdir -p %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%expat64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%expat.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%expat64.build -d %name-%version/%_arch64
%endif

%expat.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%expat64.install -d %name-%version/%_arch64
# don't need 64-bit xmlwf
rm -r $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
%endif

%expat.install -d %name-%version/%base_arch
rm $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (0755, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add BuildConflics SUNWlexpt.
* Fri Mar 23 2007 - laca@sun.com
- create
