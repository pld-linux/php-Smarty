%define		main_version 3.1.19
%define		doc_version	3.1.14
%define		php_min_version 5.2.0
Summary:	Template engine for PHP
Summary(pl.UTF-8):	System szablonów dla PHP
Name:		php-Smarty
Version:	%{main_version}
Release:	1
License:	LGPL v2.1+
Group:		Development/Languages/PHP
Source0:	http://www.smarty.net/files/Smarty-%{version}.tar.gz
# Source0-md5:	8db6f31fcf80aa0e0cbb064112fbb1bd
# Source1Download: http://www.smarty.net/documentation
Source1:	http://www.smarty.net/files/docs/manual-en.%{doc_version}.zip
# Source1-md5:	f54b1dd458776e4b1ccfdbfbfda1f484
Patch0:		path.patch
URL:		http://www.smarty.net/
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	unzip
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(mbstring)
Requires:	php(pcre)
Requires:	php(tokenizer)
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

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{appdir}
cp -a libs/* $RPM_BUILD_ROOT%{appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README SMARTY_3.1_NOTES.txt
%dir %{appdir}
%dir %{appdir}/plugins
%dir %{appdir}/sysplugins
%{appdir}/Smarty.class.php
%{appdir}/SmartyBC.class.php
%{appdir}/debug.tpl
%{appdir}/plugins/*.php
%{appdir}/sysplugins/*.php

%files doc
%defattr(644,root,root,755)
%doc demo manual-en
