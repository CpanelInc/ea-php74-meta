# Defining the package namespace
%global ns_name ea
%global ns_dir /opt/cpanel

%global _scl_prefix %{ns_dir}
%global scl_name_base    %{ns_name}-php
%global scl_macro_base   %{ns_name}_php
%global scl_name_version 74
%global scl              %{scl_name_base}%{scl_name_version}
%scl_package %scl

# do not produce empty debuginfo package
%global debug_package %{nil}

Summary:       Package that installs PHP 7.4
Name:          %scl_name
Version:       7.4.24
Vendor:        cPanel, Inc.
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define        release_prefix 1
Release:       %{release_prefix}%{?dist}.cpanel
Group:         Development/Languages
License:       GPLv2+

Source0:       macros-build
Source1:       README
Source2:       LICENSE
Source3:       whm_feature_addon

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: scl-utils-build
BuildRequires: help2man
# Temporary work-around
BuildRequires: iso-codes

Requires:      %{?scl_prefix}php-common
Requires:      %{?scl_prefix}php-cli

# Our code requires that pear be installed when the meta package is installed
Requires:      %{?scl_prefix}pear

%description
This is the main package for %scl Software Collection,
that install PHP 7.4 language.


%package runtime
Summary:   Package that handles %scl Software Collection.
Group:     Development/Languages
Requires:  scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary:   Package shipping basic build configuration
Group:     Development/Languages
Requires:  scl-utils-build

%description build
Package shipping essential configuration macros
to build %scl Software Collection.


%package scldevel
Summary:   Package shipping development files for %scl
Group:     Development/Languages

Provides:  ea-php-scldevel = %{version}
Conflicts: ea-php-scldevel > %{version}, ea-php-scldevel < %{version}

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.


%prep
%setup -c -T

cat <<EOF | tee enable
export PATH=%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF

# generate rpm macros file for depended collections
cat << EOF | tee scldev
%%scl_%{scl_macro_base}         %{scl}
%%scl_prefix_%{scl_macro_base}  %{scl_prefix}
EOF

# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat >README <<'EOF'
%{expand:%(cat %{SOURCE1})}
EOF

# copy the license file so %%files section sees it
cp %{SOURCE2} .


%build
# generate a helper script that will be used by help2man
cat >h2m_helper <<'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_helper

# generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -D -m 644 enable %{buildroot}%{_scl_scripts}/enable
install -D -m 644 scldev %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel
install -D -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/%{scl_name}.7
mkdir -p %{buildroot}/opt/cpanel/ea-php74/root/etc
mkdir -p %{buildroot}/opt/cpanel/ea-php74/root/usr/share/doc
mkdir -p %{buildroot}/opt/cpanel/ea-php74/root/usr/include
mkdir -p %{buildroot}/opt/cpanel/ea-php74/root/usr/share/man/man1
mkdir -p %{buildroot}/opt/cpanel/ea-php74/root/usr/bin
mkdir -p %{buildroot}/opt/cpanel/ea-php74/root/usr/var/cache
mkdir -p %{buildroot}/opt/cpanel/ea-php74/root/usr/var/tmp
mkdir -p %{buildroot}/opt/cpanel/ea-php74/root/usr/%{_lib}
mkdir -p %{buildroot}/usr/local/cpanel/whostmgr/addonfeatures
install %{SOURCE3} %{buildroot}/usr/local/cpanel/whostmgr/addonfeatures/%{name}

# Even if this package doesn't use it we need to do this because if another
# package does (e.g. pear licenses) it will be created and unowned by any RPM
%if 0%{?_licensedir:1}
mkdir %{buildroot}/%{_licensedir}
%endif

%scl_install

tmp_version=$(echo %{scl_name_version} | sed -re 's/([0-9])([0-9])/\1\.\2/')
sed -e 's/@SCL@/%{scl_macro_base}%{scl_name_version}/g' -e "s/@VERSION@/${tmp_version}/g" %{SOURCE0} \
  | tee -a %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config

# Remove empty share/[man|locale]/ directories
find %{buildroot}/opt/cpanel/%{scl}/root/usr/share/man/ -type d -empty -delete
find %{buildroot}/opt/cpanel/%{scl}/root/usr/share/locale/ -type d -empty -delete
mkdir -p %{buildroot}/opt/cpanel/%{scl}/root/usr/share/locale

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files


%files runtime
%defattr(-,root,root)
%doc README LICENSE
%scl_files
%{_mandir}/man7/%{scl_name}.*
%dir /opt/cpanel/ea-php74/root/etc
%dir /opt/cpanel/ea-php74/root/usr
%dir /opt/cpanel/ea-php74/root/usr/share
%dir /opt/cpanel/ea-php74/root/usr/share/doc
%dir /opt/cpanel/ea-php74/root/usr/include
%dir /opt/cpanel/ea-php74/root/usr/share/man
%dir /opt/cpanel/ea-php74/root/usr/bin
%dir /opt/cpanel/ea-php74/root/usr/var
%dir /opt/cpanel/ea-php74/root/usr/var/cache
%dir /opt/cpanel/ea-php74/root/usr/var/tmp
%dir /opt/cpanel/ea-php74/root/usr/%{_lib}
%attr(644, root, root) /usr/local/cpanel/whostmgr/addonfeatures/%{name}
%if 0%{?_licensedir:1}
%dir %{_licensedir}
%endif

%files build
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl}-config


%files scldevel
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel


%changelog
* Fri Sep 24 2021 Cory McIntire <cory@cpanel.net> - 7.4.24-1
- EA-10136: Update ea-php74 from v7.4.23 to v7.4.24

* Thu Aug 26 2021 Travis Holloway <t.holloway@cpanel.net> - 7.4.23-1
- EA-10081: Update ea-php74 from v7.4.22 to v7.4.23

* Thu Jul 29 2021 Cory McIntire <cory@cpanel.net> - 7.4.22-1
- EA-10009: Update ea-php74 from v7.4.21 to v7.4.22

* Thu Jul 01 2021 Cory McIntire <cory@cpanel.net> - 7.4.21-1
- EA-9925: Update ea-php74 from v7.4.20 to v7.4.21

* Mon Jun 28 2021 Travis Holloway <t.holloway@cpanel.net> - 7.4.20-2
- EA-9013: Optimize %check section

* Fri Jun 04 2021 Cory McIntire <cory@cpanel.net> - 7.4.20-1
- EA-9831: Update ea-php74 from v7.4.19 to v7.4.20

* Thu May 06 2021 Cory McIntire <cory@cpanel.net> - 7.4.19-1
- EA-9752: Update ea-php74 from v7.4.18 to v7.4.19

* Fri Apr 30 2021 Cory McIntire <cory@cpanel.net> - 7.4.18-1
- EA-9737: Update ea-php74 from v7.4.16 to v7.4.18

* Thu Mar 04 2021 Cory McIntire <cory@cpanel.net> - 7.4.16-1
- EA-9622: Update ea-php74 from v7.4.15 to v7.4.16

* Thu Feb 04 2021 Cory McIntire <cory@cpanel.net> - 7.4.15-1
- EA-9565: Update ea-php74 from v7.4.14 to v7.4.15

* Thu Jan 07 2021 Cory McIntire <cory@cpanel.net> - 7.4.14-1
- EA-9517: Update ea-php74 from v7.4.13 to v7.4.14

* Sun Nov 29 2020 Cory McIntire <cory@cpanel.net> - 7.4.13-1
- EA-9448: Update ea-php74 from v7.4.12 to v7.4.13

* Tue Nov 03 2020 Cory McIntire <cory@cpanel.net> - 7.4.12-1
- EA-9401: Update ea-php74 from v7.4.11 to v7.4.12

* Thu Oct 01 2020 Cory McIntire <cory@cpanel.net> - 7.4.11-1
- EA-9339: Update ea-php74 from v7.4.10 to v7.4.11

* Thu Sep 03 2020 Cory McIntire <cory@cpanel.net> - 7.4.10-1
- EA-9282: Update ea-php74 from v7.4.9 to v7.4.10

* Thu Aug 06 2020 Cory McIntire <cory@cpanel.net> - 7.4.9-1
- EA-9224: Update ea-php74 from v7.4.8 to v7.4.9

* Thu Jul 09 2020 Cory McIntire <cory@cpanel.net> - 7.4.8-1
- EA-9150: Update ea-php74 from v7.4.7 to v7.4.8

* Fri Jun 12 2020 Cory McIntire <cory@cpanel.net> - 7.4.7-1
- EA-9109: Update ea-php74 from v7.4.6 to v7.4.7

* Thu May 14 2020 Cory McIntire <cory@cpanel.net> - 7.4.6-1
- EA-9070: Update ea-php74 from v7.4.5 to v7.4.6

* Thu Apr 23 2020 Daniel Muey <dan@cpanel.net> - 7.4.5-2
- ZC-6611: Do not package empty share directories

* Thu Apr 16 2020 Cory McIntire <cory@cpanel.net> - 7.4.5-1
- EA-9007: Update ea-php74 from v7.4.2 to v7.4.5

* Wed Feb 05 2020 Daniel Muey <dan@cpanel.net> - 7.4.2-1
- EA-8867: Update ea-php74 from v7.4.1 to v7.4.2

* Tue Dec 24 2019 Daniel Muey <dan@cpanel.net> - 7.4.1-1
- ZC-5848: Initial packaging
