#
# spec file for package expat
#

Name:         expat
Version:      2.0.0
Release:      1
Summary:      libexpat - XML parser library
License:      MIT
Group:        Applications/Cryptography
URL:          http://expat.sf.net/
Source:       http://internap.dl.sourceforge.net/sourceforge/expat/expat-%{version}.tar.gz
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
James Clark''s Expat XML parser library in C. It is a stream oriented parser that requires setting handlers to deal with the structure that the parser discovers in the document.


%prep
%setup -n %{name}-%{version}

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure \
                        --prefix=%{_prefix} \
                        --libexecdir=%{_libexecdir} \
                        --libdir=%{_libdir} \
                        --bindir=%{_bindir} \
			--mandir=%{_mandir} \
			--infodir=%{_datadir}/info
make 

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -fr $RPM_BUILD_ROOT

%changelog
* Fri Mar 25 2007 - laca@sun.com
- create
