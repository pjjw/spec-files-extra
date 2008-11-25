#
# spec file for package SFEcodeina
#
# includes module(s): codeina
#
# Note there has not been a codeina tarball release.  You need to
# build a tarball by hand from SVN, and run autogen.sh, then run
# "make dist" to create a tarball to build with.  To access codeina
# from subversion:
#
# svn co https://core.fluendo.com/gstreamer/svn/codeina/trunk/ codeina
#
# bugdb: https://core.fluendo.com/gstreamer/trac/
#
%define pythonver 2.4

%include Solaris.inc

Name:           SFEcodeina
Summary:        Codec Installer
URL:            https://core.fluendo.com/gstreamer/trac/wiki/codeina
Version:        0.10.3.1
Source:         codeina-%{version}.tar.bz2
# This patch is needed since we do not yet support PyOpenSSL with
# Python 2.5 on Solaris.
#owner:yippi date:2008-11-06 type:branding
Patch1:         codeina-01-fixpython.diff
# With Firefox 3.0, this patch is necessary since libgtkmozembed is no longer
# shipped with Firefox.
#owner:yippi date:2008-11-06 type:branding
Patch2:         codeina-02-usexul.diff
# This patch is needed for codeina to properly link in libnspr.so on Solaris.
# Without this patch codeina crashes on the credit-card page.
#owner:yippi date:2008-11-06 type:bug
Patch3:         codeina-03-fixnspr.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/codeina-%{version}-build
Requires:       SUNWgnome-python-libs
Requires:       SUNWgnome-media
Requires:       SUNWgst-python
Requires:       SFEpyopenssl
Requires:       SFEpyyaml
Requires:       SUNWpython-notify
Requires:       SUNWpython-twisted
BuildRequires:  SUNWPython-devel >= %{pythonver}
BuildRequires:  SUNWgst-python
BuildRequires:  SFEpyyaml
BuildRequires:  SUNWpython-notify
BuildRequires:  SFEpyopenssl
BuildRequires:  SUNWpython-twisted

%include default-depend.inc

%description
Codeina functions as a codec installer for GStreamer applications.

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun-root
Requires: SUNWgnome-config

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n codeina-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
intltoolize --copy --force --automake
aclocal $ACLOCAL_FLAGS -I common/m4
autoconf
automake -a -c -f
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove distro-specific files that do not apply to Solaris.
rm $RPM_BUILD_ROOT%{_datadir}/codeina/logo/mandrivalinux.png
rm $RPM_BUILD_ROOT%{_datadir}/codeina/logo/ubuntu.png
rm $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/fedora*xml
rm $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/mandrivalinux*xml
rm $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/plf*xml
rm $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/ubuntu*xml

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-??_??.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/codeina
%{_bindir}/codeina.bin
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/codeina.desktop
%dir %attr (0755, root, sys) %{_datadir}/autostart
%{_datadir}/autostart/*
%{_datadir}/codeina/*

%files root
%defattr(-, root, sys)
%attr(0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/codeina/*
%{_sysconfdir}/xdg/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z][a-z].omf
#FIXME: Not in 2.22.0:%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf
%endif

%changelog
* Tue Nov 25 2008 - brian.cameron@sun.com
- Clean up spec-file
* Mon Nov 10 2008 - brian.cameron@sun.com
- Codeina depends on Twisted, so list it as a dependency.
* Wed Nov 05 2008 - brian.cameron@sun.com
- Remove codeina-02-nolsb.diff since this has been fixed upstream.
  Add codeina-03-fixnspr.diff to address crashing problem on the credit-card
  page.  Without this patch codeina can't link in libnspr.so which is needed
  for HTTPS transactions.
* Mon Oct 13 2008 - brian.cameron@sun.com
- Modify codeina to use libxul.so instead of libgtkembedmoz.so so it works
  with Firefox 3.0.
* Thu Sep 18 2008 - jijun.yu@sun.com
- Correct one dependency to SUNWpython-notify.
* Wed Jun 11 2008 - brian.cameron@sun.com
- Bump to the latest 0.10.3.1 version.
* Thu Apr 10 2008 - brian.cameron@sun.com
- New spec file. 

