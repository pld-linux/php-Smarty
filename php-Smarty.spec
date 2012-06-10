%define		doc_version	3.1.8
%define		php_min_version 5.2.0
%define     main_version 3.1.9
Summary:	Template engine for PHP
Summary(pl.UTF-8):	System szablonów dla PHP
Name:		php-Smarty
Version:	%{main_version}
Release:	1
License:	LGPL v2.1+
Group:		Development/Languages/PHP
Source0:	http://www.smarty.net/files/Smarty-%{version}.tar.gz
# Source0-md5:	eaa7cfb6fb5940f750de379674859206
# Source1Download: http://www.smarty.net/documentation
Source1:	http://www.smarty.net/files/docs/manual-en-%{doc_version}.zip
# Source1-md5:	ca37df6101a699597bff31067d9a34de
Patch0:		path.patch
URL:		http://www.smarty.net/
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	unzip
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-date
Requires:	php-mbstring
Requires:	php-pcre
Requires:	php-tokenizer
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	pear(smarty_internal_parsetree.php)
%define		appdir		%{php_data_dir}/Smarty3

%description
Smarty is a template engine for PHP. Smarty provides your basic
variable substitution and dynamic block functionality, and also takes
a step further to be a "smart" template engine, adding features such
as configuration files, template functions, variable modifiers, and
making all of this functionality as easy as possible to use for both
programmers and template designers.

%description -l pl.UTF-8
Smarty jest systemem szablonów dla PHP. Pozwala na podstawowe
podstawianie wartości zmiennych oraz dynamiczne operacje na blokach;
idzie o krok dalej, aby być "mądrym" silnikiem szablonów, dodając
takie możliwości jak pliki konfiguracyjne, funkcje, zmienne
modyfikatory oraz czyniąc całą funkcjonalność jak najłatwiejszą w
użyciu jednocześnie dla programistów i projektantów szablonów.

%package doc
Summary:	Template engine for PHP - documentation
Summary(pl.UTF-8):	System szablonów dla PHP - dokumentacja
Version:	%{doc_version}
Group:		Development/Languages/PHP

%description doc
Documentation for Smarty template engine.

%description doc -l pl.UTF-8
Dokumentacja do systemu szablonów Smarty.

%prep
%setup -q -n Smarty-%{main_version} -a1
%patch0 -p1

%undos -f php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{appdir}/{plugins,sysplugins},%{php_data_dir}}

cp -a libs/Smarty.class.php $RPM_BUILD_ROOT%{php_data_dir}
cp -a libs/debug.tpl $RPM_BUILD_ROOT%{appdir}
cp -a libs/plugins/*.php $RPM_BUILD_ROOT%{appdir}/plugins
cp -a libs/sysplugins/*.php $RPM_BUILD_ROOT%{appdir}/sysplugins

# backards compatible with entry point in subdir
ln -s ../Smarty.class.php $RPM_BUILD_ROOT%{appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README SMARTY_3.1_NOTES.txt
# entry point in include_path
%{php_data_dir}/Smarty.class.php

# app itself
%dir %{appdir}
%dir %{appdir}/plugins
%dir %{appdir}/sysplugins
%{appdir}/Smarty.class.php
%{appdir}/debug.tpl
%{appdir}/plugins/*.php
%{appdir}/sysplugins/*.php

%files doc
%defattr(644,root,root,755)
%doc demo/*
