#
# spec file for package SFEopenmotif
#
# includes module(s): OpenMotif
#

%include Solaris.inc
%define src_name        openmotif
%define X11_DIR %{_prefix}/X11

Name:                    SFEopenmotif
Summary:                 OpenMotif is the publicly licensed version of Motif, the industry standard user interface toolkit for UNIX systems.
Version:                 2.3.0
Source:                  ftp://ftp.ics.com/openmotif/2.3/2.3.0/openmotif-%{version}.tar.gz
URL:                     http://www.motifzone.net/index.php
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Patch0:                  %{src_name}-01-%{version}.diff
Patch1:                  %{src_name}-02-compatibility.diff
Source1:                 XmStrDefs21.ht

%include default-depend.inc

Requires: SUNWcsu
Requires: SUNWxwxft
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWfontconfig
Requires: SFEfreetype
BuildRequires: SFEfreetype-devel
Conflicts: SUNWmfrun
Conflicts: SUNWmfdev

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}
Conflicts: SUNWmfdev

%prep
%setup -q -n openmotif-%version
%patch0 -p1

%build
./configure --prefix=%{X11_DIR} \
            --mandir=%{X11_DIR}/share/man \
            --sysconfdir=%{_sysconfdir} \
            --enable-xft \
            --enable-jpeg \
            --enable-png \
            --with-freetype-config=%{gnu_bin}/freetype-config

cat %{PATCH1} | gpatch -p1 --fuzz=0
cp %{SOURCE1} lib/Xm

make

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf ${RPM_BUILD_ROOT}/%{_prefix}/share
rm -rf ${RPM_BUILD_ROOT}/%{X11_DIR}/man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{X11_DIR}
%dir %attr (0755, root, bin) %{X11_DIR}/bin
%{X11_DIR}/bin/*
%dir %attr (0755, root, bin) %{X11_DIR}/lib
%{X11_DIR}/lib/*
%dir %attr(0755, root, bin) %{X11_DIR}/share
%dir %attr(0755, root, bin) %{X11_DIR}/share/man
%dir %attr(0755, root, bin) %{X11_DIR}/share/man/man1
%{X11_DIR}/share/man/man1/*
%dir %attr(0755, root, bin) %{X11_DIR}/share/man/man3
%{X11_DIR}/share/man/man3/*
%dir %attr(0755, root, bin) %{X11_DIR}/share/man/man4
%{X11_DIR}/share/man/man4/*
%dir %attr(0755, root, bin) %{X11_DIR}/share/man/man5
%{X11_DIR}/share/man/man5/*
%dir %attr(0755, root, bin) %{X11_DIR}/share/man/manm
%{X11_DIR}/share/man/manm/*

%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/pixmaps
%{X11_DIR}/share/Xm/pixmaps/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{X11_DIR}
%dir %attr (0755, root, bin) %{X11_DIR}/include
%{X11_DIR}/include/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/ButtonBox/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Color/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Column/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Exm
%{X11_DIR}/share/Xm/Exm/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Ext18list
%{X11_DIR}/share/Xm/Ext18list/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Icon/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Outline/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Paned2/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Tabstack/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/Tree/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/airport/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/animate/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/autopopups/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/combo2/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/draw/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/earth/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/filemanager/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/fileview/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/fontsel/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/getsubres/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/helloint/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/hellomotif/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/i18ninput/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/panner/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/periodic/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/piano/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/sampler2_0/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/setDate/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/todo/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/tooltips/*
%dir %attr (0755, root, bin) %{X11_DIR}/share/Xm/wsm/*

%changelog
* Thu Feb 07 2008 - moinak.ghosh@sun.com
- Rework to add compatibility with Solaris Motif.
- Add devel package.
- Change install prefix to /usr/X11
- Update dependencies.
- Thu Feb 07 2008 - pradhap (at) gmail.com
- Initial openmotif spec file.

