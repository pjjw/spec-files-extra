# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	streamripper
%define src_version	1.62.3
%define pkg_release	1

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	streamripper : audio stream ripper
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPL
Source:         http://nchc.dl.sourceforge.net/sourceforge/streamripper/%{src_name}-%{version}.tar.gz
#Patch:        	yourpatch-name
URL:            http://streamripper.sourceforge.net
Packager:     	Shivakumar GN
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build

#Requires:      
#BuildRequires: 

%description 
You can use it to rip (copy) streams of the following kinds:

   1. .mp3 Shoutcast streams - the kind of streams found on shoutcast.com.
   2. .mp3 Icecast streams - a GNU GPL/Open Source version of Shoutcast. Both Icecast 1.x and Icecast 2.x are supported. However, UDP metadata is not supported for Icecast 1.x.
   3. .nvs (Nullsoft Streaming Video) streams - which Winamp tv uses.
   4. .aac Shoutcast/Icecast streams - the kind of streams found on tuner2.com. NOTE: Streamripper can't rip RealAudio AAC streams, only shoutcast/icecast AAC.
   5. .ogg streams - these streams are found at dir.xiph.org.

Streamripper can't help with ripping stuff like RealPlayer, Windows MediaPlayer, MusicMatch or anything else similar.

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
CC=gcc
export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib"
./configure --prefix=%{_prefix}

#%patch0 -p 1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
make

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Install-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File permissions, ownership information. Note the difference between 
# bin(_bindir),share(_datadir) & share/applications
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/man

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Dec 30 2007 - markwright@internode.on.net
- Bump to 1.62.3
* 2007.Aug.11 - <shivakumar dot gn at gmail dot com>
- Initial spec.
