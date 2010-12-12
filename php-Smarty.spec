%define		doc_version	3.0
%define		php_min_version 5.2.0
%include	/usr/lib/rpm/macros.php
Summary:	Template engine for PHP
Summary(pl.UTF-8):	System szablonów dla PHP
Name:		Smarty3
Version:	3.0.5
Release:	0.1
License:	LGPL v2.1+
Group:		Development/Languages/PHP
Source0:	http://www.smarty.net/files/%{name}-%{version}.tar.gz
# Source0-md5:	f7483eaa36ec72337827060076296478
# Source1Download: http://www.smarty.net/documentation
Source1:	http://www.smarty.net/files/docs/manual-en-%{doc_version}.zip
# Source1-md5:	8db376266f1313927cc8e112f2526e21
Source2:	%{name}-function.html_input_image.php
Patch0:		path.patch
Patch1:		modifier.mb_truncate.patch
URL:		http://www.smarty.net/
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	unzip
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-date
Requires:	php-pcre
Requires:	php-tokenizer
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		appdir	%{php_data_dir}/Smarty3

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
%setup -q -a1
%patch0 -p1
cp -a libs/plugins/modifier.{,mb_}truncate.php
#%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{appdir}/{plugins,sysplugins},%{php_pear_dir}}

cp -a libs/Smarty.class.php $RPM_BUILD_ROOT%{php_data_dir}
cp -a libs/debug.tpl $RPM_BUILD_ROOT%{appdir}
cp -a libs/plugins/*.php $RPM_BUILD_ROOT%{appdir}/plugins
cp -a libs/sysplugins/*.php $RPM_BUILD_ROOT%{appdir}/sysplugins
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{appdir}/plugins/function.html_input_image.php

# backards compatible with pear dir
ln -s %{appdir} $RPM_BUILD_ROOT%{php_pear_dir}/%{name}

# backards compatible with entry point in subdir
ln -s ../Smarty.class.php $RPM_BUILD_ROOT%{appdir}

%clean
rm -rf $RPM_BUILD_ROOT

# make compat symlink, the symlink is discarded using %ghost on package uninstall
%triggerpostun -- Smarty < 2.6.10-4
if [ -d %{php_pear_dir}/%{name}/plugins ]; then
	mv %{php_pear_dir}/%{name}/plugins/* %{appdir}/plugins
	rmdir %{php_pear_dir}/%{name}/plugins 2>/dev/null
fi
rmdir %{php_pear_dir}/%{name} 2>/dev/null || mv -v %{php_pear_dir}/%{name}{,.rpmsave}
ln -s %{appdir} %{php_pear_dir}/%{name}

%post
[ -e %{php_pear_dir}/%{name} ] || ln -s %{appdir} %{php_pear_dir}/%{name}

%files
%defattr(644,root,root,755)
%doc README SMARTY2_BC_NOTES
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

# for the sake of bc when installed to pear dir
%ghost %{php_pear_dir}/%{name}

%files doc
%defattr(644,root,root,755)
%doc demo/*
