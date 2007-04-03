#
# This package is named SFEruby-fastercsv instead of just SFEfastercsv
# because when a ruby (or perl or php) package delivers a library (as opposed
# to an application or commands) it seems to make more sense to include the
# language name in the package name.
#
#
%include Solaris.inc

Name:                SFEruby-fastercsv
Summary:             Improved, faster CSV library for Ruby
Version:             1.2.0
Source:              http://rubyforge.org/frs/download.php/17269/fastercsv-%{version}.tgz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEruby
Requires: SFEruby

%prep
%setup -q -n fastercsv-%{version}

%build
# The ruby setup.rb standard needs the following setup steps before install.
# (So unlike python's setup.py, don't bypass the build block.)
ruby setup.rb config
ruby setup.rb setup

%install
# The --prefix option when used in the context below sets the fake install
# path ($RPM_BUILD_ROOT), not the real installation prefix. The real
# installation prefix (usually /usr) and any other build/install vars are
# derived from the system when "ruby setup.rb config" is run above.

rm -rf $RPM_BUILD_ROOT
ruby setup.rb install --prefix=${RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* 
* Mon Apr 02 2007 - Eric Boutilier
