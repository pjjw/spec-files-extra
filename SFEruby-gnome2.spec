#
# spec file for package SFEruby-gnome2.spec
#
# includes module(s): ruby-gnome2
#
%include Solaris.inc

%define src_name	ruby-gnome2
%define src_url		http://nchc.dl.sourceforge.net/sourceforge/ruby-gnome2

Name:                   SFEruby-gnome2
Summary:                Ruby gnome2 bindings
Version:                0.16.0
Source:                 %{src_url}/%{src_name}-all-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEruby

%prep
%setup -q -n %{src_name}-all-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
ruby extconf.rb
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}

%changelog
* Sun May 13 2007 - dougs@truemail.co.th
- Initial version
