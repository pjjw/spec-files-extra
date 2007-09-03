#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEdeluge
Summary:             Deluge - BitTorrent client
Version:             0.5.4.1
Source:              http://download.deluge-torrent.org/tarball/0.5.4.1/deluge-0.5.4.1.tar.gz
Patch1:              deluge-01-sunpro.diff
Patch2:              deluge-02-path.diff
Patch3:              deluge-03-sparsefile.diff
URL:                 http://deluge-torrent.org/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWPython
BuildRequires: SUNWopenssl-include
BuildRequires: SFEboost-devel
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-python-libs
Requires: SUNWPython
Requires: SUNWopenssl-libraries
Requires: SUNWzlib
Requires: SFEboost
Requires: SFEpython-xdg

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%define pythonver 2.4

%prep
%setup -q -n deluge-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
# patch prefix before building
ed -s src/common.py <<'/EOF/' >/dev/null
,s:@datadir@:%_prefix:
w
q
/EOF/

%build
# workaround for pycc being invoked instead of pyCC
export PYCC_CC="$CXX"
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D__EXTENSIONS__ -I/usr/sfw/include \
 -library=stlport4 -staticlib=stlport4 -mt \
 -norunpath -features=tmplife -features=tmplrefstatic"
export CFLAGS="$CXXFLAGS"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib \
 -library=stlport4 -staticlib=stlport4 -lCrun -mt \
 -lpthread -lm -lsocket -lnsl -lcrypto"
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix=$RPM_BUILD_ROOT%{_prefix}

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/deluge
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/deluge
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/deluge
%{_datadir}/deluge/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/deluge.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Sep 02 2007 - trisk@acm.jhu.edu
- Fix Studio patch, fix file allocation issue
* Fri Aug 31 2007 - trisk@acm.jhu.edu
- Initial spec
