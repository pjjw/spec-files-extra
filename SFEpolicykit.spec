#
# spec file for package SFEpolicykit
#
# includes module(s): PolicyKit PolicyKit-gnome
#
# Issues:
#
# - There is a bug in this spec file that you need to add the polkitu user
#   and polkitg group before running the spec file.  It probably doesn't
#   make sense to try to add these in a postrun script since that gets
#   run after the package is installed, and these packages install files
#   that use this owner/group.
#
# - Currently setting libdir to /usr/lib/polkit so this package does not
#   conflict with the PolicyKit installed with HAL.  Not sure if this is
#   right or not.
#
# Owner: jim
#
%include Solaris.inc

%use policykit = PolicyKit.spec

Name:                    SFEpolicykit
Summary:                 A framework for defining policy for system-wide components
Version:                 0.7
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SUNWdbus-devel
BuildRequires: SUNWdbus-bindings-devel
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWdbus
Requires: SUNWdbus-bindings
Requires: SUNWgnome-base-libs


%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files 
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%policykit.prep -d %name-%version

%build
export RPM_OPT_FLAGS="$CFLAGS"
%policykit.build -d %name-%version

%install
%policykit.install -d %name-%version

# -f used because charset alias doesn't seem to be created when using
# gnu libiconv/libintl
rm -f $RPM_BUILD_ROOT%{_libdir}/polkit/charset.alias
rm -f $RPM_BUILD_ROOT%{_libdir}/polkit/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/polkit/*.a
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/polkit-bash-completion.sh
rm -fr $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
rm -fr $RPM_BUILD_ROOT%{_datadir}/applications
rm -f $RPM_BUILD_ROOT%{_datadir}/var/lib/misc/PolicyKit.reload

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -f $RPM_BUILD_ROOT%{_libdir}/polkit/PolicyKit/modules/*.{la,ai}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'groupadd -g 220 polkitg';
  echo 'useradd -u 220 -d %{_datadir}/empty -c "PolicyKit User" -g polkitg polkitu';
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS -a

%post
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'umask 022';
  echo 'touch %{_basedir}/var/lib/misc/PolicyKit.reload';
  echo 'chown root:politg %{_basedir}/var/lib/misc/PolicyKit.reload';
  echo 'chmod 664 %{_basedir}/var/lib/misc/PolicyKit.reload';
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS -a

%postun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'userdel polkitu';
  echo 'groupdel polkitg';
)

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/polkit-action
%{_bindir}/polkit-auth
%{_bindir}/polkit-config-file-validate
%{_bindir}/polkit-policy-file-validate
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/polkit/lib*.so*
%attr(2755,root,polkitg) %{_libexecdir}/polkit/polkit-explicit-grant-helper
%attr(2755,root,polkitg) %{_libexecdir}/polkit/polkit-grant-helper
%attr(4755,root,polkitg) %{_libexecdir}/polkit/polkit-grant-helper-pam
%attr(2755,root,polkitg) %{_libexecdir}/polkit/polkit-read-auth-helper
%attr(2755,root,polkitg) %{_libexecdir}/polkit/polkit-revoke-helper
%attr(2755,root,polkitg) %{_libexecdir}/polkit/polkit-set-default-helper
%{_libexecdir}/polkit/polkitd
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, root) %{_datadir}/PolicyKit
%{_datadir}/PolicyKit/config.dtd
%dir %attr (0755, root, root) %{_datadir}/PolicyKit/policy
%{_datadir}/PolicyKit/policy/*
%{_datadir}/dbus-1/interfaces/org.freedesktop.PolicyKit.AuthenticationAgent.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.PolicyKit.service
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0755, root, bin) %{_mandir}/man5
%dir %attr(0755, root, bin) %{_mandir}/man8
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files root
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr (0755, root, sys) %dir %{_sysconfdir}/PolicyKit
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PolicyKit/PolicyKit.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PolicyKit.conf
%dir %attr (0755, root, root) %{_sysconfdir}/pam.d
%{_sysconfdir}/pam.d/polkit
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/run
%attr(770,root,polkitg) %{_localstatedir}/run/PolicyKit
%dir %attr (0755, root, other) %{_localstatedir}/lib
%attr(770,root,polkitg) %{_localstatedir}/lib/PolicyKit
%attr(775,root,polkitg) %{_localstatedir}/lib/PolicyKit-public
%attr(775,root,polkitg) %{_localstatedir}/lib/misc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/polkit/pkgconfig
%{_libdir}/polkit/pkgconfig/polkit.pc
%{_libdir}/polkit/pkgconfig/polkit-dbus.pc
%{_libdir}/polkit/pkgconfig/polkit-grant.pc
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/PolicyKit
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, bin) %{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%endif

%changelog
* Wed Feb 06 2008 - Brian.Cameron@sun.com
- Cleanup
* Thu Jan 31 2008 - Jim.li@sun.com
- initial SFE release.
