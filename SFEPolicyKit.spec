#
# spec file for package SFEpolicykit
#
# includes module(s): PolicyKit PolicyKit-gnome
#
# Owner: jim
#
%include Solaris.inc

%use policykit = PolicyKit.spec
%use policykitgnome = PolicyKit-gnome.spec
Name:                    SFEpolicykit
Summary:                 A framework for defining policy for system-wide components
Version:                 0.7
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%define         _libexecdir     %{_basedir}/libexec

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
%policykitgnome.prep -d %name-%version

%build
export LD_LIBRARY_PATH="%{_builddir}/%{name}-%{version}/%{policykit.name}-%{policykit.version}/src/polkit/.libs:%{_builddir}/%{name}-%{version}/%{policykit.name}-%{policykit.version}/src/polkit-grant/.libs:%{_builddir}/%{name}-%{version}/%{policykit.name}-%{policykit.version}/src/polkit-dbus/.libs"
export LD_RUN_PATH="%{_builddir}/%{name}-%{version}/%{policykit.name}-%{policykit.version}/src/polkit/.libs:%{_builddir}/%{name}-%{version}/%{policykit.name}-%{policykit.version}/src/polkit-grant/.libs:%{_builddir}/%{name}-%{version}/%{policykit.name}-%{policykit.version}/src/polkit-dbus/.libs"
export LDFLAGS="%_ldflags -lpolkit-grant -lexpat"
export CFLAGS="-I../../%{policykit.name}-%{policykit.version}/src %optflags"
export PATH=%{_builddir}/%{name}-%{version}/%{policykit.name}-%{policykit.version}/tools:$PATH
export PKG_CONFIG_PATH=%{_builddir}/%{name}-%{version}/%{policykit.name}-%{policykit.version}/data:%{_pkg_config_path}
export RPM_OPT_FLAGS="$CFLAGS"
%policykit.build -d %name-%version
%policykitgnome.build -d %name-%version

%install
%policykit.install -d %name-%version
%policykitgnome.install -d %name-%version

# -f used because charset alias doesn't seem to be created when using
# gnu libiconv/libintl
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/polkit-bash-completion.sh
rm -fr $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
rm -f $RPM_BUILD_ROOT%{_datadir}/applications/polkit-gnome-authorization.desktop
rm -fr $RPM_BUILD_ROOT%{_datadir}/applications
rm -f $RPM_BUILD_ROOT%{_datadir}/var/lib/misc/PolicyKit.reload


%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -f $RPM_BUILD_ROOT%{_libdir}/PolicyKit/modules/*.{la,ai}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'groupadd -g 220 polkitg';
  echo 'useradd -u 220 -d %{_datadir}/empty -c "PolicyKit User -g polkitg polkitu';
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
%dir %attr (0755, root, bin) %{_libexecdir}
%attr(2755,root,polkitg) %{_libexecdir}/polkit-explicit-grant-helper
%attr(2755,root,polkitg) %{_libexecdir}/polkit-grant-helper
%attr(4755,root,polkitg) %{_libexecdir}/polkit-grant-helper-pam
%attr(2755,root,polkitg) %{_libexecdir}/polkit-read-auth-helper
%attr(2755,root,polkitg) %{_libexecdir}/polkit-revoke-helper
%attr(2755,root,polkitg) %{_libexecdir}/polkit-set-default-helper
%{_libexecdir}/polkitd
%{_datadir}/PolicyKit
%{_datadir}/dbus-1/interfaces/org.freedesktop.PolicyKit.AuthenticationAgent.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.PolicyKit.service
%attr(770,root,polkitg) %{_basedir}/var/lib/PolicyKit
%attr(775,root,polkitg) %{_basedir}/var/lib/PolicyKit-public
%attr(770,root,polkitg) %{_basedir}/var/run/PolicyKit
%attr(775,root,polkitg) %{_basedir}/var/lib/misc
%{_mandir}/man1/polkit-action.1*
%{_mandir}/man1/polkit-auth.1*
%{_mandir}/man1/polkit-config-file-validate.1*
%{_mandir}/man1/polkit-policy-file-validate.1*
%{_mandir}/man5/PolicyKit.conf.5*
%{_mandir}/man8/PolicyKit.8*
%{_libdir}/libpolkit.so
%{_libdir}/libpolkit.so.*.*.*
%{_libdir}/libpolkit.so.2
%{_libdir}/libpolkit-dbus.so
%{_libdir}/libpolkit-dbus.so.*.*.*
%{_libdir}/libpolkit-dbus.so.2
%{_libdir}/libpolkit-grant.so
%{_libdir}/libpolkit-grant.so.*.*.*
%{_libdir}/libpolkit-grant.so.2

%{_bindir}/polkit-gnome-authorization
%{_bindir}/polkit-gnome-example
%{_libexecdir}/polkit-gnome-manager
%{_datadir}/dbus-1/services/org.gnome.PolicyKit.service
%{_datadir}/dbus-1/services/org.gnome.PolicyKit.AuthorizationManager.service
%{_datadir}/dbus-1/services/gnome-org.freedesktop.PolicyKit.AuthenticationAgent.service
%{_libdir}/libpolkit-gnome.so.*.*.*
%{_libdir}/libpolkit-gnome.so.0

%files root
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}/PolicyKit
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PolicyKit/PolicyKit.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PolicyKit.conf
%{_sysconfdir}/pam.d/polkit


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_libdir}
%attr (-, root, bin) %{_datadir}/gtk-doc
# %dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/polkit.pc
%{_libdir}/pkgconfig/polkit-dbus.pc
%{_libdir}/pkgconfig/polkit-grant.pc
%{_libdir}/pkgconfig/polkit-gnome.pc
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/PolicyKit

%{_libdir}/libpolkit-gnome.so
# %{_includedir}/PolicyKit/polkit-gnome
%if %build_l10n
%files l10n
%defattr (-, root, bin)
%endif

%changelog
* Thu Jan 31 2007 - Jim.li@sun.com
- initial SFE release.
