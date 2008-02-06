#
# spec file for package SFEopenmotif
#
# includes module(s): OpenMotif
#

%include Solaris.inc
%define src_name        openmotif


Name:                    SFEopenmotif
Summary:                 OpenMotif is the publicly licensed version of Motif, the industry standard user interface toolkit for UNIX systems.
Version:                 2.3.0
Source:                  ftp://ftp.ics.com/openmotif/2.3/2.3.0/openmotif-%{version}.tar.gz
URL:                     http://www.motifzone.net/index.php
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Patch0:                  %{src_name}-01-%{version}.diff

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n openmotif-%version
%patch0 -p1

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man4/*
%dir %attr(0755, root, bin) %{_mandir}/man5/*
%dir %attr(0755, root, bin) %{_mandir}/manm/*

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%dir %attr (0755, root, sys) %{_datadir}/Xm
%{_datadir}/Xm/*


%changelog
- Thu Feb 07 2008 - pradhap (at) gmail.com
- Initial openmotif spec file.

