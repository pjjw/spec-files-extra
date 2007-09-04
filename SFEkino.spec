#
# spec file for package SFEkino
#
# includes module(s): kino
#
%include Solaris.inc
%use kino = kino.spec

Name:		SFEkino
Summary:	%{kino.summary}
Version:	%{kino.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibiec61883-devel
Requires: SFElibiec61883
BuildRequires: SFElibraw1394-devel
Requires: SFElibraw1394
BuildRequires: SFElibdv-devel
Requires: SFElibdv
BuildRequires: SFElibsamplerate-devel
Requires: SFElibsamplerate

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%kino.prep -d %name-%version/%{base_arch}

%build
%kino.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%kino.install -d %name-%version/%{base_arch}
find $RPM_BUILD_ROOT%{_libdir} -name \*.la -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/kino
%{_bindir}/ffmpeg-kino
%{_bindir}/kino2raw
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/kino
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (-, root, root) %{_datadir}/mime
%attr (-, root, root) %{_datadir}/mime/*

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Thu Sep  4 2007 - dougs@truemail.co.th
- Initial version
