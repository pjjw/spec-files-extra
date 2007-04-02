#   
#
%include Solaris.inc

Name:                SFEruby-facets
Summary:             Large set of base extensions/libraries for Ruby
Version:             1.8.54
Source:              http://rubyforge.org/frs/download.php/18700/facets-%{version}.tgz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEruby
Requires: SFEruby

%prep
%setup -q -n facets-%{version}

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
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/facets
%{_datadir}/facets/*

%changelog
* 
* Mon Apr 02 2007 - Eric Boutilier
